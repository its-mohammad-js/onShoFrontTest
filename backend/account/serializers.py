from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from account.models import User, Role, Permission, Organizer, ManualUser, RolePermission


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    login_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['phone_number'] = user.phone_number

        return token

    def validate(self, attrs):
        try:
            # بررسی نوع لاگین قبل از احراز هویت
            login_type = attrs.get('login_type', '').strip().lower() if attrs.get('login_type') else ''
            
            # فراخوانی validate از کلاس والد (این کار احراز هویت را انجام می‌دهد)
            data = super().validate(attrs)
            
            # بعد از احراز هویت، کاربر در self.user موجود است
            user = self.user
            
            # بررسی role کاربر
            user_role_slug = user.role.slug if user.role and user.role.slug else None
            
            # بررسی اینکه آیا کاربر organizer است یا نه
            # استفاده از try-except برای بررسی وجود organizer
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
                    raise AuthenticationFailed("شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش کاربر عادی استفاده کنید.")
            elif login_type == 'user':
                # کاربر نباید organizer باشد یا role "آموزشگاه" داشته باشد
                if is_organization_user:
                    raise AuthenticationFailed("شما اجازه لاگین از این بخش را ندارید. لطفاً از بخش سازمان/آموزشگاه استفاده کنید.")
            
            return {
                'status': True,
                'data': {
                    'token': data['access'],
                    'refresh': data['refresh'],
                }
            }
        except AuthenticationFailed as e:
            return {
                'status': False,
                'data': {
                    'error': str(e) if str(e) else "نام کاربری یا رمز عبور اشتباه است."
                }
            }


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            return {
                'status': True,
                'data': {
                    'token': data['access']
                }
            }
        except Exception as e:
            return {
                'status': False,
                'data': {
                    'error': "رفرش توکن معتبر نیست."
                }
            }


class UserProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField()
    role = serializers.CharField(source='role.slug', read_only=True)  # فقط عنوان نقش
    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']

    def get_city(self, obj):
        return obj.city.id if obj.city else ""

    def get_province(self, obj):
        return obj.province.id if obj.province else ""

    def get_permissions(self, obj):
        """دریافت لیست `slug` های پرمیژن‌های کاربر به صورت یک آرایه ساده"""
        if obj.role:
            return list(obj.role.permissions.values_list('permission__slug', flat=True))
        return []


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'birthday', 'email', 'gender', 'role', 'city', 'province',
                  'meli_code', 'age']


class SendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # تنظیم نقش به صورت پیش‌فرض به "دانشجو"
        try:
            role = Role.objects.get(slug='دانشجو')  # اسلاگ نقش دانشجو "دانشجو" است
        except Role.DoesNotExist:
            raise serializers.ValidationError({'role': 'Default role "دانشجو" does not exist'})

        validated_data['role'] = role

        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True, min_length=8)
    confirmPassword = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirmPassword": "رمز عبور جدید با تکرار آن مطابقت ندارد."})

        return data


# -----------------------------------------------------------------------------------------------------------------------
# this is for permissions
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'title', 'slug']


# -----------------------------------------------------------------------------------------------------------------------
# Organization Registration Serializer
class OrganizationRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True)
    national_card = serializers.ImageField(required=True)
    license = serializers.ImageField(required=True)
    subdomain = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value.startswith('09') or len(value) != 11:
            raise serializers.ValidationError("شماره موبایل باید 11 رقم و با 09 شروع شود.")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("کاربری با این شماره تلفن از قبل وجود دارد.")
        return value

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("ایمیل از قبل وجود دارد.")
        return value

    def validate(self, data):
        """Validate password match"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'رمز عبور و تکرار آن مطابقت ندارند.'})
        return data

    def create(self, validated_data):
        """Create User and Organizer"""
        # دریافت role "مدیر-کل" برای organizer
        # اگر role وجود نداشت، خطا بده (باید از seed data ایجاد شده باشد)
        try:
            role = Role.objects.get(slug='مدیر-کل')
        except Role.DoesNotExist:
            # اگر role وجود نداشت، سعی می‌کنیم با title پیدا کنیم
            try:
                role = Role.objects.get(title='مدیر کل')
            except Role.DoesNotExist:
                # اگر باز هم پیدا نشد، role را ایجاد می‌کنیم با همه permissions
                role, created = Role.objects.get_or_create(
                    title='مدیر کل',
                    defaults={'slug': 'مدیر-کل'}
                )
                
                # اگر role جدید ایجاد شد، همه permissions را به آن اضافه می‌کنیم
                if created:
                    all_permissions = [
                        'course_create', 'course_edit', 'course_delete', 'course_view',
                        'lesson_create', 'lesson_edit', 'lesson_delete', 'lesson_view',
                        'user_manage', 'order_manage', 'payment_manage', 'webinar_manage',
                        'ticket_manage', 'comment_manage', 'rating_manage', 'file_upload',
                        'task_create', 'task_grade', 'task_view', 'chat_manage'
                    ]
                    
                    # ایجاد یا دریافت permission ها و اضافه کردن به role
                    for perm_slug in all_permissions:
                        permission, _ = Permission.objects.get_or_create(
                            slug=perm_slug,
                            defaults={'title': perm_slug.replace('_', ' ').title()}
                        )
                        
                        # اضافه کردن permission به role
                        RolePermission.objects.get_or_create(
                            role=role,
                            permission=permission
                        )

        # Extract user data
        user_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'phone_number': validated_data['phone_number'],
            'password': validated_data['password'],
            'role': role,
        }

        # Create user
        user = User.objects.create_user(**user_data)

        # Create organizer name from user's full name
        organizer_name = f"{validated_data['first_name']} {validated_data['last_name']}"

        # Create organizer with logo (using license as temporary logo)
        organizer = Organizer.objects.create(
            user=user,
            name=organizer_name,
            description='',  # Can be updated later
            logo=validated_data['license'],  # Using license as temporary logo (can be updated later)
            national_card=validated_data['national_card'],
            license=validated_data['license'],
            subdomain=validated_data.get('subdomain', None),  # Subdomain is optional
            is_active=True,
            is_verified=False,  # Needs admin verification
        )

        return user


# -----------------------------------------------------------------------------------------------------------------------
# Manual User Serializer
class ManualUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualUser
        fields = ['id', 'name', 'lastname', 'nationalcode', 'tel', 'birthdate', 'address', 'career', 'create_date', 'update_date']
        read_only_fields = ['id', 'create_date', 'update_date']

    def validate_nationalcode(self, value):
        """Validate national code format and uniqueness"""
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("کد ملی باید 10 رقم باشد.")
        if ManualUser.objects.filter(nationalcode=value).exists():
            raise serializers.ValidationError("کاربری با این کد ملی از قبل وجود دارد.")
        return value

    def validate_tel(self, value):
        """Validate phone number format"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("شماره تلفن باید 11 رقم باشد.")
        return value
