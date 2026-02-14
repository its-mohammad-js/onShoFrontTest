from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from account.authentication import CustomJWTAuthentication
from course.models import CourseUser
from .models import Order, Status, PurchaseCode, CodeRedemption
from .serializers import (
    OrderCreateSerializer, PurchaseCodeCreateSerializer, 
    PurchaseCodeSerializer, CodeRedeemSerializer, CodeRedemptionSerializer
)


class OrderCreateView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                # Save the order using the serializer
                order = serializer.save()

                # Prepare response data
                response_data = {
                    "order_id": order.id,
                    "status": order.status.title,
                    "total_price": order.total_price,
                    "courses": [
                        {
                            "course_id": course_order.course.id,
                            "title": course_order.course.title,
                            "quantity": course_order.quantity,
                            "price": course_order.price,
                            "discount": course_order.discount,
                            "final_price": course_order.final_price
                        }
                        for course_order in order.course_orders.all()
                    ]
                }
                return Response({"status": True, "data": response_data}, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Check if it's a validation error
                if hasattr(e, 'detail') and isinstance(e.detail, dict):
                    return Response({"status": False, "data": e.detail}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status": False, "data": {"error": str(e)}},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user).prefetch_related('course_orders__course')

        # ساختن لیست سفارشات
        orders_data = []
        for order in orders:
            orders_data.append({
                "order_id": order.id,
                "status": order.status.title,
                "total_price": order.total_price,
                "create_date": order.create_date,
                "update_date": order.update_date,
                "courses": [
                    {
                        "course_id": course_order.course.id,
                        "title": course_order.course.title,
                        "quantity": course_order.quantity,
                        "price": course_order.price,
                        "discount": course_order.discount,
                        "final_price": course_order.final_price
                    }
                    for course_order in order.course_orders.all()
                ]
            })

        return Response({"status": True, "data": orders_data}, status=status.HTTP_200_OK)


class PaymentCompleteView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response({
                "status": False,
                "data": {"error": "Order ID is required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the order
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Order not found or you don't have permission to access it."}
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if order is already completed
        if order.status.slug == 'completed':
            return Response({
                "status": False,
                "data": {"error": "Order is already completed."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Update order status to completed
            completed_status = Status.objects.get(slug='completed')
            order.status = completed_status
            order.save()

            # Create course enrollments
            from course.models import CourseUser
            enrolled_courses = []
            
            for course_order in order.course_orders.all():
                # Create or update course enrollment
                course_user, created = CourseUser.objects.get_or_create(
                    course=course_order.course,
                    user=request.user,
                    defaults={'status': 'not_started'}
                )
                enrolled_courses.append({
                    'course_id': course_order.course.id,
                    'title': course_order.course.title,
                    'enrolled': True
                })

            return Response({
                "status": True,
                "data": {
                    "message": "Payment completed successfully!",
                    "order_id": order.id,
                    "status": order.status.title,
                    "enrolled_courses": enrolled_courses
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": f"Error completing payment: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentGatewayInitView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response({
                "status": False,
                "data": {"error": "Order ID is required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the order
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Order not found or you don't have permission to access it."}
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if order is already paid
        if order.status.slug == 'completed':
            return Response({
                "status": False,
                "data": {"error": "Order is already paid."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            from .gateways import ZarinpalGateway, IDPayGateway
            from django.conf import settings
            from django.urls import reverse
            
            # Check if test mode is enabled
            test_mode = getattr(settings, 'PAYMENT_TEST_MODE', True)
            
            if test_mode:
                # Test mode - simulate successful payment
                from .models import PaymentGateway, Transaction, Situation
                
                # Create test gateway
                gateway_obj, created = PaymentGateway.objects.get_or_create(
                    name='test',
                    defaults={
                        'display_name': 'تست',
                        'is_active': True,
                        'is_sandbox': True
                    }
                )
                
                pending_situation, created = Situation.objects.get_or_create(
                    slug='pending',
                    defaults={'title': 'در انتظار پرداخت'}
                )
                
                # Create test transaction
                test_authority = f"test_{order.id}_{order.user.id}"
                transaction = Transaction.objects.create(
                    order=order,
                    gateway=gateway_obj,
                    situation=pending_situation,
                    ref_number=test_authority,
                    gateway_transaction_id=test_authority,
                    authority=test_authority,
                    payment_url=f"/payment/callback?Authority={test_authority}&Status=OK",
                    price=order.total_price,
                    gateway_response={'test_mode': True}
                )
                
                return Response({
                    "status": True,
                    "data": {
                        "payment_url": f"/payment/callback?Authority={test_authority}&Status=OK",
                        "transaction_id": transaction.id,
                        "gateway": "test",
                        "test_mode": True
                    }
                }, status=status.HTTP_200_OK)
            
            # Get payment gateway
            gateway_name = getattr(settings, 'PAYMENT_GATEWAY', 'zarinpal')
            
            # Prepare payment data
            amount = order.total_price  # Amount in Toman
            description = f"پرداخت سفارش شماره {order.id}"
            callback_url = request.build_absolute_uri(reverse('payment-callback'))
            
            # Initialize gateway
            if gateway_name == 'zarinpal':
                gateway = ZarinpalGateway(
                    merchant_id=getattr(settings, 'ZARINPAL_MERCHANT_ID', ''),
                    sandbox=getattr(settings, 'ZARINPAL_SANDBOX', True)
                )
                
                # Create payment request
                result = gateway.create_payment_request(
                    amount=amount,
                    description=description,
                    callback_url=callback_url,
                    mobile=request.user.phone_number,
                    email=getattr(request.user, 'email', None)
                )
                
            elif gateway_name == 'idpay':
                gateway = IDPayGateway(
                    api_key=getattr(settings, 'IDPAY_API_KEY', ''),
                    sandbox=getattr(settings, 'IDPAY_SANDBOX', True)
                )
                
                # Create payment request
                result = gateway.create_payment_request(
                    amount=amount * 10,  # Convert Toman to Rial for IDPay
                    order_id=order.id,
                    description=description,
                    callback_url=callback_url,
                    name=f"{request.user.first_name} {request.user.last_name}".strip(),
                    phone=request.user.phone_number,
                    mail=getattr(request.user, 'email', None)
                )
            else:
                return Response({
                    "status": False,
                    "data": {"error": "Invalid payment gateway configuration."}
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if result['success']:
                # Create transaction record
                from .models import PaymentGateway, Transaction, Situation
                
                gateway_obj, created = PaymentGateway.objects.get_or_create(
                    name=gateway_name,
                    defaults={
                        'display_name': 'زرین‌پال' if gateway_name == 'zarinpal' else 'آیدی‌پی',
                        'is_active': True,
                        'is_sandbox': getattr(settings, f'{gateway_name.upper()}_SANDBOX', True)
                    }
                )
                
                pending_situation, created = Situation.objects.get_or_create(
                    slug='pending',
                    defaults={'title': 'در انتظار پرداخت'}
                )
                
                transaction = Transaction.objects.create(
                    order=order,
                    gateway=gateway_obj,
                    situation=pending_situation,
                    ref_number=result.get('authority') or result.get('payment_id', ''),
                    gateway_transaction_id=result.get('authority') or result.get('payment_id', ''),
                    authority=result.get('authority', ''),
                    payment_url=result.get('payment_url', ''),
                    price=amount,
                    gateway_response=result
                )
                
                return Response({
                    "status": True,
                    "data": {
                        "payment_url": result['payment_url'],
                        "transaction_id": transaction.id,
                        "gateway": gateway_name
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "data": {"error": result['error']}
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": f"Error initializing payment: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentCallbackView(APIView):
    """
    Handle payment gateway callback
    """
    
    def get(self, request, *args, **kwargs):
        # Get callback parameters
        authority = request.GET.get('Authority')
        payment_status = request.GET.get('Status')
        
        if not authority:
            return Response({
                "status": False,
                "data": {"error": "Missing authority parameter."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find transaction
            from .models import Transaction, Situation
            transaction = Transaction.objects.get(authority=authority)
            
            if payment_status == 'OK':
                # Check if this is a test transaction
                if transaction.gateway.name == 'test' or authority.startswith('test_'):
                    # Test mode - simulate successful payment
                    result = {
                        'success': True,
                        'ref_id': f"test_ref_{transaction.id}",
                        'card_pan': '****1234'
                    }
                else:
                    # Verify payment with real gateway
                    from .gateways import ZarinpalGateway, IDPayGateway
                    from django.conf import settings
                    
                    gateway_name = getattr(settings, 'PAYMENT_GATEWAY', 'zarinpal')
                    
                    if gateway_name == 'zarinpal':
                        gateway = ZarinpalGateway(
                            merchant_id=getattr(settings, 'ZARINPAL_MERCHANT_ID', ''),
                            sandbox=getattr(settings, 'ZARINPAL_SANDBOX', True)
                        )
                    
                        result = gateway.verify_payment(
                            authority=authority,
                            amount=transaction.price
                        )
                        
                    elif gateway_name == 'idpay':
                        gateway = IDPayGateway(
                            api_key=getattr(settings, 'IDPAY_API_KEY', ''),
                            sandbox=getattr(settings, 'IDPAY_SANDBOX', True)
                        )
                        
                        result = gateway.verify_payment(
                            payment_id=transaction.gateway_transaction_id,
                            order_id=transaction.order.id
                        )
                
                if result['success']:
                    # Update transaction
                    success_situation, created = Situation.objects.get_or_create(
                        slug='success',
                        defaults={'title': 'پرداخت موفق'}
                    )
                    
                    transaction.situation = success_situation
                    transaction.ref_number = result.get('ref_id') or result.get('track_id', '')
                    transaction.card_mask = result.get('card_pan', '')
                    transaction.gateway_response = result
                    transaction.save()
                    
                    # Complete the payment directly
                    try:
                        # Update order status to completed
                        completed_status = Status.objects.get(slug='completed')
                        transaction.order.status = completed_status
                        transaction.order.save()

                        # Create course enrollments
                        from course.models import CourseUser
                        enrolled_courses = []
                        
                        for course_order in transaction.order.course_orders.all():
                            # Create or update course enrollment
                            course_user, created = CourseUser.objects.get_or_create(
                                course=course_order.course,
                                user=transaction.order.user,
                                defaults={'status': 'in_progress'}
                            )
                            enrolled_courses.append({
                                'course_id': course_order.course.id,
                                'title': course_order.course.title,
                                'enrolled': True
                            })

                        return Response({
                            "status": True,
                            "data": {
                                "message": "پرداخت با موفقیت انجام شد!",
                                "order_id": transaction.order.id,
                                "ref_id": transaction.ref_number,
                                "enrolled_courses": enrolled_courses
                            }
                        }, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({
                            "status": False,
                            "data": {"error": f"خطا در تکمیل پرداخت: {str(e)}"}
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    # Payment failed
                    failed_situation, created = Situation.objects.get_or_create(
                        slug='failed',
                        defaults={'title': 'پرداخت ناموفق'}
                    )
                    
                    transaction.situation = failed_situation
                    transaction.gateway_response = result
                    transaction.save()
                    
                    return Response({
                        "status": False,
                        "data": {"error": result['error']}
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # User cancelled payment
                cancelled_situation, created = Situation.objects.get_or_create(
                    slug='cancelled',
                    defaults={'title': 'لغو شده توسط کاربر'}
                )
                
                transaction.situation = cancelled_situation
                transaction.save()
                
                return Response({
                    "status": False,
                    "data": {"error": "پرداخت توسط کاربر لغو شد."}
                }, status=status.HTTP_400_BAD_REQUEST)

        except Transaction.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Transaction not found."}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": f"Error processing callback: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationPurchaseCodeCreateView(APIView):
    """
    Organization users can purchase courses and receive codes.
    They can buy multiple codes for a course, each with a specified number of credits.
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        # Check if user has an organization
        user = request.user
        try:
            organizer = user.organizer
        except:
            return Response({
                "status": False,
                "data": {"error": "User is not associated with an organization"}
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = PurchaseCodeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            course_id = serializer.validated_data['course_id']
            quantity = serializer.validated_data['quantity']  # Number of codes to generate
            credits_per_code = serializer.validated_data['credits_per_code']  # Credits per code

            course = Course.objects.get(id=course_id)

            # Create purchase order for the organization (if needed for tracking)
            # For now, we'll just create the codes directly
            created_codes = []
            
            for _ in range(quantity):
                purchase_code = PurchaseCode.objects.create(
                    course=course,
                    organization=organizer,
                    purchased_by=user,
                    total_credits=credits_per_code,
                    remaining_credits=credits_per_code,
                    is_active=True
                )
                created_codes.append({
                    'code': purchase_code.code,
                    'course_title': course.title,
                    'total_credits': purchase_code.total_credits,
                    'remaining_credits': purchase_code.remaining_credits,
                    'created_at': purchase_code.create_date
                })

            return Response({
                "status": True,
                "data": {
                    "message": f"Successfully created {len(created_codes)} purchase code(s)",
                    "codes": created_codes
                }
            }, status=status.HTTP_201_CREATED)

        except Course.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Course not found"}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": f"Error creating purchase codes: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationPurchaseCodeListView(APIView):
    """
    List all purchase codes created by the organization
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            organizer = user.organizer
        except:
            return Response({
                "status": False,
                "data": {"error": "User is not associated with an organization"}
            }, status=status.HTTP_403_FORBIDDEN)

        purchase_codes = PurchaseCode.objects.filter(
            organization=organizer
        ).select_related('course').order_by('-create_date')

        serializer = PurchaseCodeSerializer(purchase_codes, many=True)
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class CourseListView(APIView):
    """
    List all available courses for organization users to view
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        from course.serializers import CourseSerializer
        from course.models import Course
        
        courses = Course.objects.all().select_related('category', 'organizer', 'standard').prefetch_related('rates')
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class CodeRedeemView(APIView):
    """
    Normal users can redeem a code to purchase a course.
    If the code has credits, the course will be purchased and one credit will be deducted.
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        user = request.user
        
        serializer = CodeRedeemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_str = serializer.validated_data['code']
            purchase_code = PurchaseCode.objects.get(code=code_str)

            # Check if code can be used
            can_use, error_message = purchase_code.can_be_used()
            if not can_use:
                return Response({
                    "status": False,
                    "data": {"error": error_message}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already enrolled in this course
            if CourseUser.objects.filter(course=purchase_code.course, user=user).exists():
                return Response({
                    "status": False,
                    "data": {"error": "You are already enrolled in this course"}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already redeemed this code for this course
            if CodeRedemption.objects.filter(code=purchase_code, user=user, course=purchase_code.course).exists():
                return Response({
                    "status": False,
                    "data": {"error": "You have already redeemed this code for this course"}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Use one credit from the code
            if not purchase_code.use_credit():
                return Response({
                    "status": False,
                    "data": {"error": "Failed to use code credit"}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create course enrollment
            course_user, created = CourseUser.objects.get_or_create(
                course=purchase_code.course,
                user=user,
                defaults={'status': 'not_started'}
            )

            # Record the redemption
            redemption = CodeRedemption.objects.create(
                code=purchase_code,
                user=user,
                course=purchase_code.course
            )

            return Response({
                "status": True,
                "data": {
                    "message": "Code redeemed successfully! Course purchased.",
                    "code": purchase_code.code,
                    "course": {
                        "id": purchase_code.course.id,
                        "title": purchase_code.course.title
                    },
                    "remaining_credits": purchase_code.remaining_credits,
                    "enrollment_status": course_user.status
                }
            }, status=status.HTTP_200_OK)

        except PurchaseCode.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Invalid code"}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": f"Error redeeming code: {str(e)}"}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCodeRedemptionsListView(APIView):
    """
    List all code redemptions by the current user
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        
        redemptions = CodeRedemption.objects.filter(user=user).select_related('code', 'course').order_by('-redeemed_at')
        serializer = CodeRedemptionSerializer(redemptions, many=True)
        
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)