import random

import random
import logging
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import status

logger = logging.getLogger(__name__)
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .authentication import CustomJWTAuthentication
from .models import UserOtp, User, Permission, ManualUser
from .sms_service import SMSService
from .serializers import (CustomTokenObtainSerializer, CustomTokenRefreshSerializer, UserProfileSerializer,
                          UserProfileEditSerializer, UserRegisterSerializer, ChangePasswordSerializer,
                          PermissionSerializer, OrganizationRegisterSerializer, ManualUserSerializer)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken as e:
            return Response(
                {
                    "status": "error",
                    "detail": "نام کاربری یا رمز عبور اشتباه است."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        response_data = serializer.validated_data
        if response_data.get('status', False):
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({"data": {"message": "Successfully logged out."}}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        # بررسی وضعیت احراز هویت کاربر
        if not user.is_authenticated:
            return Response({
                "status": False,
                "data": {
                    "error": "Authentication credentials were not provided or are invalid."
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        # استفاده از سریالایزر برای بازگشت داده‌های پروفایل
        serializer = UserProfileSerializer(user)
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserProfileEditView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = UserProfileEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "data": {
                "error": "Invalid data",
                "details": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)


class SendOTPCodeView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        login_type = request.data.get("login_type", '').strip().lower() if request.data.get("login_type") else ''

        # اعتبارسنجی شماره تلفن
        if not phone_number or len(phone_number) != 11 or not phone_number.startswith("09"):
            return Response({'status': False, 'data': {"error": "Invalid phone number."}},
                            status=status.HTTP_400_BAD_REQUEST)

        # بررسی وجود شماره تلفن در جدول User
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response({'status': False, 'data': {"error": "Phone number not registered."}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # اگر کاربر وجود دارد، بررسی تطابق login_type با role کاربر
        if user:
            user_role_slug = user.role.slug if user.role and user.role.slug else None
            
            # بررسی اینکه آیا کاربر organizer است یا نه
            try:
                is_organizer = user.organizer is not None
            except:
                is_organizer = False
            
            # نقش‌های سازمان/آموزشگاه
            organization_roles = ['آموزشگاه', 'organization', 'institute', 'organizer']
            is_organization_user = (user_role_slug in organization_roles) or is_organizer
            
            # بررسی تطابق نوع لاگین با نوع کاربر
            # اگر login_type مشخص نشده باشد، به صورت پیش‌فرض 'user' در نظر می‌گیریم
            if not login_type:
                login_type = 'user'
            
            if login_type in ['organization', 'institute', 'organizer']:
                # کاربر باید organizer باشد یا role "آموزشگاه" داشته باشد
                if not is_organization_user:
                    return Response({
                        'status': False,
                        'data': {"error": "شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش کاربر عادی استفاده کنید."}
                    }, status=status.HTTP_403_FORBIDDEN)
            elif login_type == 'user':
                # کاربر نباید organizer باشد یا role "آموزشگاه" داشته باشد
                if is_organization_user:
                    return Response({
                        'status': False,
                        'data': {"error": "شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش سازمان/آموزشگاه استفاده کنید."}
                    }, status=status.HTTP_403_FORBIDDEN)

        # بررسی یا ایجاد OTP
        number = UserOtp.objects.filter(phone_number=phone_number, delete_date__isnull=True,
                                        expire_date__gte=timezone.now()).first()

        code = str(random.randint(10000, 100000))

        if number is None:
            UserOtp.objects.create(
                phone_number=phone_number,
                code=code,
                expire_date=timezone.now() + timezone.timedelta(minutes=4)
            )
        else:
            diff_minutes = (number.expire_date - timezone.now()).total_seconds() / 60
            if diff_minutes > 0:
                if number.used_count < 5:
                    number.expire_date = timezone.now() + timezone.timedelta(minutes=4)
                    number.used_count += 1
                    number.code = code
                    number.save()
                else:
                    number.expire_date = timezone.now() + timezone.timedelta(minutes=2 * diff_minutes)
                    number.used_count += 1
                    number.save()

                    return Response(
                        {
                            'status': True,
                            'data': {"error": "This number has been used too many times. Please try again later."}
                        },
                        status=status.HTTP_429_TOO_MANY_REQUESTS)

            else:
                UserOtp.objects.create(
                    phone_number=phone_number,
                    code=code,
                    expire_date=timezone.now() + timezone.timedelta(minutes=4)
                )

        # Send OTP via SMS using the new SMS service
        sms_service = SMSService()
        sms_result = sms_service.send_otp_sms(phone_number, code)
        
        if sms_result['status']:
            return Response({
                'status': True,
                'data': {
                    "message": "OTP sent successfully via SMS.",
                    "code": code  # Keep code in response for testing purposes
                }
            }, status=status.HTTP_200_OK)
        else:
            # If SMS fails, still return the code but log the error
            logger.error(f"SMS sending failed: {sms_result.get('error', 'Unknown error')}")
            return Response({
                'status': True,
                'data': {
                    "message": "OTP generated but SMS failed. Using development mode.",
                    "code": code,
                    "sms_error": sms_result.get('error', 'Unknown error'),
                    "development_mode": True
                }
            }, status=status.HTTP_200_OK)

        # PRODUCTION SMS SENDING CODE (commented out for development)
        # api_url = "https://api.kavenegar.com/v1/5779456F555A797971462F356C39785976713678336371365972376C4C3941714938374E557A7462327A553D/verify/lookup.json/"
        # payload = {
        #     "receptor": phone_number,
        #     "token": code,
        #     "template": "verify5plus2"
        # }

        # try:
        #     response = requests.post(api_url, data=payload)
        #     response_data = response.json()

        #     if response.status_code == 200:
        #         return Response({
        #             'status': True,
        #             'data': {
        #                 "message": "OTP sent successfully.",
        #                 "code": code
        #             }
        #         }, status=status.HTTP_200_OK)
        #     else:
        #         return Response({
        #             'status': False,
        #             'data': {
        #                 "error": f"Failed to send SMS. Error: {response_data.get('message', 'Unknown error')}"
        #             }
        #         }, status=response.status_code)

        # except Exception as e:
        #     return Response({
        #         'status': False,
        #         'data': {
        #             "error": f"An error occurred while sending SMS: {str(e)}"
        #         }
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckOTPCodeView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = request.data.get("code")
        login_type = request.data.get("login_type", '').strip().lower() if request.data.get("login_type") else ''

        if not phone_number or not otp_code:
            return Response({
                "status": False,
                "data": {
                    "error": "Phone number and OTP code are required."
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        number = UserOtp.objects.filter(
            phone_number=phone_number,
            code=otp_code,
            expire_date__gte=timezone.now(),
            delete_date__isnull=True,
            used_count__lt=5
        ).first()

        if not number:
            return Response({
                "status": False,
                "data": {
                    "error": "Invalid OTP code."
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()
        user_created = False
        if not user:
            user = User.objects.create(phone_number=phone_number)
            user_created = True
        
        # بررسی role کاربر و تطابق با login_type (فقط برای کاربران موجود)
        if not user_created:
            user_role_slug = user.role.slug if user.role and user.role.slug else None
            
            # بررسی اینکه آیا کاربر organizer است یا نه
            try:
                is_organizer = user.organizer is not None
            except:
                is_organizer = False
            
            # نقش‌های سازمان/آموزشگاه
            organization_roles = ['آموزشگاه', 'organization', 'institute', 'organizer']
            is_organization_user = (user_role_slug in organization_roles) or is_organizer
            
            # بررسی تطابق نوع لاگین با نوع کاربر
            # اگر login_type مشخص نشده باشد، به صورت پیش‌فرض 'user' در نظر می‌گیریم
            if not login_type:
                login_type = 'user'
            
            if login_type in ['organization', 'institute', 'organizer']:
                # کاربر باید organizer باشد یا role "آموزشگاه" داشته باشد
                # توجه: در اینجا چک is_verified انجام نمی‌شود - کاربران وریفای نشده هم می‌توانند لاگین کنند
                # چک is_verified فقط در CourseCreateView و سایر viewهای مرتبط با ایجاد دوره انجام می‌شود
                if not is_organization_user:
                    return Response({
                        "status": False,
                        "data": {
                            "error": "شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش کاربر عادی استفاده کنید."
                        }
                    }, status=status.HTTP_403_FORBIDDEN)
            elif login_type == 'user':
                # کاربر نباید organizer باشد یا role "آموزشگاه" داشته باشد
                if is_organization_user:
                    return Response({
                        "status": False,
                        "data": {
                            "error": "شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش سازمان/آموزشگاه استفاده کنید."
                        }
                    }, status=status.HTTP_403_FORBIDDEN)

        # ایجاد توکن - کاربران وریفای نشده هم می‌توانند لاگین کنند
        # محدودیت ایجاد دوره برای کاربران وریفای نشده در CourseCreateView اعمال می‌شود
        refresh = RefreshToken.for_user(user)

        number.delete_date = timezone.now()
        number.save()
        return Response({
            "status": True,
            "data": {
                "message": "OTP verified successfully.",
                "token": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send welcome SMS after successful registration
            try:
                sms_service = SMSService()
                user_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else None
                sms_result = sms_service.send_welcome_sms(user.phone_number, user_name)
                
                if not sms_result['status']:
                    logger.warning(f"Welcome SMS failed for user {user.phone_number}: {sms_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"Error sending welcome SMS: {str(e)}")
            
            return Response({
                'status': True,
                'message': 'User registered successfully',
                'data': {
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role.slug
                }
            }, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'data': {'errors': serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationRegisterView(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = OrganizationRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send welcome SMS after successful registration
            try:
                sms_service = SMSService()
                user_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else None
                sms_result = sms_service.send_welcome_sms(user.phone_number, user_name)
                
                if not sms_result['status']:
                    logger.warning(f"Welcome SMS failed for user {user.phone_number}: {sms_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"Error sending welcome SMS: {str(e)}")
            
            return Response({
                'status': True,
                'message': 'Organization registered successfully',
                'data': {
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role.slug if user.role else None
                }
            }, status=status.HTTP_201_CREATED)
        
        # Format errors for better frontend handling
        errors = {}
        for field, error_list in serializer.errors.items():
            if isinstance(error_list, list):
                errors[field] = error_list[0] if error_list else 'Invalid value'
            else:
                errors[field] = str(error_list)
        
        return Response({
            'status': False,
            'data': {'errors': errors}
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        old_password = serializer.validated_data.get('oldPassword')
        new_password = serializer.validated_data.get('newPassword')

        # بررسی رمز عبور فعلی
        if not check_password(old_password, user.password):
            return Response({
                "status": False,
                "data": {"oldPassword": "رمز عبور فعلی نادرست است."}
            }, status=status.HTTP_400_BAD_REQUEST)

        # تغییر رمز عبور
        user.set_password(new_password)
        user.save()

        return Response({
            "status": True,
            "data": {"message": "رمز عبور با موفقیت تغییر یافت."}
        }, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------------------------
# this is for permissions

class PermissionListAPIView(APIView):

    def post(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response({"status": True, "data": serializer.data})


class UserRolePermissionListAPIView(APIView):
    """API که فقط پرمیژن‌های مرتبط با نقش کاربر احراز هویت شده را برمی‌گرداند."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.role:
            return Response({"status": False, "data": "شما هیچ نقشی ندارید."}, status=403)

        # دریافت پرمیژن‌های نقش کاربر
        role_permissions = user.role.permissions.values_list("permission__id", "permission__title", "permission__slug")
        permissions_data = [{"id": perm[0], "title": perm[1], "slug": perm[2]} for perm in role_permissions]

        return Response({"status": True, "data": permissions_data})


class GoogleLoginView(APIView):
    """Get Google OAuth URL or redirect directly to Google"""
    
    def get(self, request):
        from django.conf import settings
        from django.shortcuts import redirect
        from urllib.parse import urlencode
        
        frontend_redirect_uri = request.GET.get('redirect_uri', 'http://localhost:3000/auth/google/callback')
        return_json = request.GET.get('json', 'false').lower() == 'true'
        
        # Store frontend redirect URI in session for later use
        request.session['google_redirect_uri'] = frontend_redirect_uri
        
        # Build Google OAuth URL
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        
        if not client_id or client_id == '':
            if return_json:
                return Response({
                    "status": False,
                    "data": {"error": "Google OAuth Client ID not configured. Please set GOOGLE_OAUTH2_CLIENT_ID in .env file."}
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # For direct redirect, show error page
            return Response({
                "status": False,
                "data": {"error": "Google OAuth not configured"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Backend callback URL (where Google will redirect after auth)
        # Use configured redirect URI if available, otherwise build from request
        if hasattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI') and settings.GOOGLE_OAUTH2_REDIRECT_URI:
            backend_callback_url = settings.GOOGLE_OAUTH2_REDIRECT_URI
        else:
            # Build absolute URI and ensure HTTPS in production
            backend_callback_url = request.build_absolute_uri('/auth/google/callback')
            # If behind proxy (nginx), ensure HTTPS is used for production domains
            if not settings.DEBUG:
                # Force HTTPS for production domains
                if 'onsho24.ir' in backend_callback_url and backend_callback_url.startswith('http://'):
                    backend_callback_url = backend_callback_url.replace('http://', 'https://')
        
        # Log the redirect URI for debugging (remove in production if needed)
        logger.debug(f"Google OAuth redirect URI: {backend_callback_url}")
        
        # Build the Google OAuth URL
        params = {
            'client_id': client_id,
            'redirect_uri': backend_callback_url,  # Google redirects to backend
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        
        # If json=true, return JSON response with auth_url
        if return_json:
            return Response({
                "status": True,
                "data": {
                    "auth_url": google_auth_url
                }
            })
        
        # Otherwise, redirect directly to Google
        return redirect(google_auth_url)


class GoogleCallbackView(APIView):
    """Handle Google OAuth callback - can accept code or access_token"""
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    authentication_classes = []  # No authentication required for OAuth callback
    permission_classes = []  # No permission required for OAuth callback
    
    def get(self, request):
        """Handle GET request from Google redirect (with code)"""
        import requests
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.conf import settings
        from django.shortcuts import redirect
        from urllib.parse import urlencode
        from .serializers import UserProfileSerializer
        
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
            error_url = f"{redirect_uri}?error={error}"
            return redirect(error_url)
        
        if not code:
            redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
            error_url = f"{redirect_uri}?error=no_code"
            return redirect(error_url)
        
        try:
            # Get backend callback URL (must match what we sent to Google)
            # Use configured redirect URI if available, otherwise build from request
            if hasattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI') and settings.GOOGLE_OAUTH2_REDIRECT_URI:
                backend_callback_url = settings.GOOGLE_OAUTH2_REDIRECT_URI
            else:
                # Build absolute URI and ensure HTTPS in production
                backend_callback_url = request.build_absolute_uri('/auth/google/callback')
                # If behind proxy (nginx), ensure HTTPS is used
                if not settings.DEBUG and 'onsho24.ir' in backend_callback_url:
                    backend_callback_url = backend_callback_url.replace('http://', 'https://')
            
            # Exchange code for access token
            token_response = requests.post('https://oauth2.googleapis.com/token', data={
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': backend_callback_url,  # Must match what we sent to Google
                'grant_type': 'authorization_code'
            })
            
            if token_response.status_code != 200:
                redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
                error_url = f"{redirect_uri}?error=token_exchange_failed"
                return redirect(error_url)
            
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            if not access_token:
                redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
                error_url = f"{redirect_uri}?error=no_access_token"
                return redirect(error_url)
            
            # Get user info from Google
            user_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                params={'access_token': access_token}
            )
            
            if user_response.status_code != 200:
                redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
                error_url = f"{redirect_uri}?error=user_info_failed"
                return redirect(error_url)
            
            google_user_data = user_response.json()
            email = google_user_data.get('email')
            
            if not email:
                redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
                error_url = f"{redirect_uri}?error=no_email"
                return redirect(error_url)
            
            # Get or create user
            user, created = self.get_or_create_user(google_user_data)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token_jwt = refresh.access_token
            
            # Get redirect URI from session
            redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
            
            # Build redirect URL with tokens
            token_params = {
                'token': str(access_token_jwt),
                'refresh': str(refresh),
                'status': 'success'
            }
            
            redirect_url = f"{redirect_uri}?{urlencode(token_params)}"
            return redirect(redirect_url)
            
        except Exception as e:
            logger.error(f"Google OAuth error: {str(e)}")
            redirect_uri = request.session.get('google_redirect_uri', 'http://localhost:3000/auth/google/callback')
            error_url = f"{redirect_uri}?error=server_error&message={str(e)}"
            return redirect(error_url)
    
    def post(self, request):
        """Handle POST request with code or access_token"""
        import requests
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.conf import settings
        from .serializers import UserProfileSerializer
        
        # Debug: log request data (using info level so it shows in production)
        logger.info(f"Google callback POST - Content-Type: {request.content_type}")
        
        # IMPORTANT: Read request.body FIRST before accessing request.data
        # In DRF, once you access request.data, you cannot access request.body anymore
        body_content = None
        if hasattr(request, '_body'):
            body_content = request._body
        elif hasattr(request, 'body'):
            try:
                body_content = request.body
            except Exception as e:
                logger.warning(f"Could not read request.body: {str(e)}")
        
        if body_content:
            logger.info(f"Google callback POST - request.body (first 200 chars): {body_content[:200] if len(body_content) > 200 else body_content}")
        else:
            logger.info(f"Google callback POST - request.body: Empty")
        
        # Try to get code and access_token from request.data
        code = None
        access_token = None
        
        try:
            if hasattr(request, 'data'):
                code = request.data.get('code')
                access_token = request.data.get('access_token')
                logger.info(f"Google callback POST - From request.data: code={code is not None}, access_token={access_token is not None}")
                logger.info(f"Google callback POST - request.data: {request.data}")
        except Exception as e:
            logger.warning(f"Could not access request.data: {str(e)}")
        
        # Fallback: try to parse JSON from body_content if request.data is empty
        if not code and not access_token and body_content:
            try:
                import json
                body_data = json.loads(body_content.decode('utf-8'))
                code = body_data.get('code')
                access_token = body_data.get('access_token')
                logger.info(f"Google callback POST - Parsed from body: code={code is not None}, access_token={access_token is not None}")
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.error(f"Google callback POST - Failed to parse JSON from body: {str(e)}")
                if body_content:
                    logger.error(f"  Body content: {body_content.decode('utf-8', errors='ignore')[:500]}")
        
        logger.info(f"Google callback POST - Final: code={'Present' if code else 'Missing'}, access_token={'Present' if access_token else 'Missing'}")
        
        # If code is provided, exchange it for access token
        if code:
            try:
                # Get backend callback URL (must match what we sent to Google)
                # برای POST request، باید از URL که در Google Console ثبت شده استفاده کنیم
                if hasattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI') and settings.GOOGLE_OAUTH2_REDIRECT_URI:
                    backend_callback_url = settings.GOOGLE_OAUTH2_REDIRECT_URI
                    logger.info(f"Google callback POST - Using redirect_uri from settings: {backend_callback_url}")
                else:
                    # Build absolute URI - باید دقیقاً همان URL باشد که در Google Console ثبت شده
                    # اگر از /api/auth/google/callback استفاده می‌کنید، باید آن را در Google Console هم ثبت کنید
                    if request.path.startswith('/api/'):
                        backend_callback_url = request.build_absolute_uri('/api/auth/google/callback')
                    else:
                        backend_callback_url = request.build_absolute_uri('/auth/google/callback')
                    
                    # Ensure HTTPS in production
                    if not settings.DEBUG and 'onsho24.ir' in backend_callback_url:
                        backend_callback_url = backend_callback_url.replace('http://', 'https://')
                    
                    logger.info(f"Google callback POST - Built redirect_uri from request: {backend_callback_url}")
                
                logger.info(f"Google callback POST - Exchanging code. backend_callback_url: {backend_callback_url}")
                logger.info(f"Google callback POST - Code: {code[:20]}..." if code and len(code) > 20 else f"Google callback POST - Code: {code}")
                
                # Exchange code for access token
                token_response = requests.post('https://oauth2.googleapis.com/token', data={
                    'code': code,
                    'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                    'redirect_uri': backend_callback_url,
                    'grant_type': 'authorization_code'
                })
                
                logger.info(f"Google callback POST - Token exchange response status: {token_response.status_code}")
                
                if token_response.status_code != 200:
                    error_data = token_response.json() if token_response.content else {}
                    logger.error(f"Token exchange failed: {token_response.status_code} - {error_data}")
                    logger.error(f"  Used redirect_uri: {backend_callback_url}")
                    logger.error(f"  Code: {code[:50]}..." if code and len(code) > 50 else f"  Code: {code}")
                    return Response({
                        "status": False,
                        "data": {
                            "error": "Failed to exchange code for access token",
                            "details": error_data,
                            "redirect_uri_used": backend_callback_url
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                token_data = token_response.json()
                access_token = token_data.get('access_token')
                
                if not access_token:
                    return Response({
                        "status": False,
                        "data": {"error": "No access token received from Google"}
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except Exception as e:
                logger.error(f"Error exchanging code for token: {str(e)}")
                return Response({
                    "status": False,
                    "data": {"error": f"Error exchanging code: {str(e)}"}
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # If no code and no access_token, return error
        if not access_token:
            # Log more details for debugging
            logger.error(f"Google callback POST - No code or access_token provided.")
            logger.error(f"  request.data: {request.data}")
            logger.error(f"  request.POST: {request.POST}")
            logger.error(f"  request.body: {request.body}")
            logger.error(f"  request.content_type: {request.content_type}")
            logger.error(f"  request.path: {request.path}")
            
            # Try to return more helpful error message
            error_msg = "Either 'code' or 'access_token' must be provided"
            if not code and not access_token:
                if request.body:
                    error_msg += f". Received body: {request.body.decode('utf-8', errors='ignore')[:200]}"
                else:
                    error_msg += ". No data received in request body."
            
            return Response({
                "status": False,
                "data": {
                    "error": error_msg,
                    "received_data": dict(request.data) if hasattr(request, 'data') and request.data else "No data",
                    "request_path": request.path,
                    "content_type": request.content_type
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get user info from Google
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                params={'access_token': access_token}
            )
            
            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                logger.error(f"Failed to get user info: {response.status_code} - {error_data}")
                return Response({
                    "status": False,
                    "data": {"error": "Invalid access token", "details": error_data}
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            google_user_data = response.json()
            email = google_user_data.get('email')
            
            if not email:
                return Response({
                    "status": False,
                    "data": {"error": "Email not provided by Google"}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get or create user
            user, created = self.get_or_create_user(google_user_data)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token_jwt = refresh.access_token
            
            # Serialize user data
            user_serializer = UserProfileSerializer(user, context={'request': request})
            
            return Response({
                "status": True,
                "data": {
                    "token": str(access_token_jwt),
                    "refresh": str(refresh),
                    "user": user_serializer.data,
                    "is_new_user": created
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Google OAuth error: {str(e)}")
            return Response({
                "status": False,
                "data": {"error": f"An error occurred: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_or_create_user(self, google_data):
        """Get existing user by email or create new one"""
        from account.models import Role
        
        email = google_data.get('email')
        first_name = google_data.get('given_name', '')
        last_name = google_data.get('family_name', '')
        picture = google_data.get('picture', '')
        
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            # Update user info if needed
            if not user.first_name and first_name:
                user.first_name = first_name
            if not user.last_name and last_name:
                user.last_name = last_name
            if not user.email_verified_date:
                user.email_verified_date = timezone.now()
                user.is_verified = True
            user.save()
            return user, False
        except User.DoesNotExist:
            # Create new user
            # Generate unique phone number
            phone_number = f"09{email[:9].replace('@', '').replace('.', '')[:9]}"
            counter = 1
            original_phone = phone_number
            while User.objects.filter(phone_number=phone_number).exists():
                phone_number = f"{original_phone[:-1]}{counter}"
                counter += 1
                if counter > 99:
                    import time
                    phone_number = f"09{str(int(time.time()))[-9:]}"
                    break
            
            # Get default role
            try:
                role = Role.objects.get(slug='دانشجو')
            except Role.DoesNotExist:
                role = None
            
            user = User.objects.create_user(
                phone_number=phone_number,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                email_verified_date=timezone.now(),
                is_verified=True,
            )
            
            return user, True


class ManualUserCreateView(APIView):
    """Create a new manual user"""
    parser_classes = [JSONParser, MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = ManualUserSerializer(data=request.data)
        
        if serializer.is_valid():
            manual_user = serializer.save()
            return Response({
                "status": True,
                "data": ManualUserSerializer(manual_user).data,
                "message": "کاربر دستی با موفقیت ایجاد شد."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "خطا در ایجاد کاربر دستی."
        }, status=status.HTTP_400_BAD_REQUEST)
