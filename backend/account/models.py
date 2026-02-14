import random
import logging
import re

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    meli_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True, max_length=180)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, related_name='users', blank=True, null=True)
    province = models.ForeignKey('Province', on_delete=models.SET_NULL, related_name='users', blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True, choices=(('M', 'Male'), ('F', 'Female')))
    birthday = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    user_image = models.ImageField(upload_to='user', blank=True, null=True)
    phone_verified_date = models.DateTimeField(blank=True, null=True)
    email_verified_date = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def gender_display(self):
        return self.get_gender_display()  # مقدار نمایشی gender

    def has_permission(self, permission_slug):
        """بررسی دسترسی کاربر بر اساس نقش"""
        return self.role and self.role.has_permission(permission_slug)

    def __str__(self):
        return self.phone_number


class Organizer(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, related_name='organizer')
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    website_url = models.URLField(blank=True, null=True)
    subdomain = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name='زیردامنه',
        help_text='زیردامنه اختصاصی آموزشگاه (مثال: sazman) - فقط نام subdomain بدون .onsho24.ir'
    )
    
    national_card = models.ImageField(upload_to='organizer/documents', blank=True, null=True)
    license = models.ImageField(upload_to='organizer/documents', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    display_order = models.IntegerField(default=9999, verbose_name='اولویت نمایش در صفحه اصلی', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Clean and validate subdomain before saving
        if self.subdomain:
            # فقط نام subdomain را بگیر (بدون .onsho24.ir یا هر چیز دیگری)
            subdomain = self.subdomain.strip().lower()
            # حذف کاراکترهای غیرمجاز و فقط alphanumeric و dash و underscore
            subdomain = re.sub(r'[^a-z0-9_-]', '', subdomain)
            # حذف .onsho24.ir اگر وجود داشته باشد
            subdomain = subdomain.replace('.onsho24.ir', '')
            subdomain = subdomain.replace('onsho24.ir', '')
            self.subdomain = subdomain.strip()
        
        # Check if is_verified is being changed from False to True
        was_verified = False
        is_new = self.pk is None
        if self.pk:
            try:
                old_instance = Organizer.objects.get(pk=self.pk)
                was_verified = old_instance.is_verified
            except Organizer.DoesNotExist:
                pass
        
        # Generate slug
        if self.name:
            base_slug = slugify(self.name, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Organizer.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        
        # Save the instance
        super().save(*args, **kwargs)
        
        # اگر organizer جدید ایجاد شد، role کاربر را به "مدیر-کل" تغییر بده
        if is_new and self.user:
            try:
                admin_role = Role.objects.get(slug='مدیر-کل')
                if self.user.role != admin_role:
                    self.user.role = admin_role
                    self.user.save(update_fields=['role'])
            except Role.DoesNotExist:
                # اگر role "مدیر-کل" وجود نداشت، سعی می‌کنیم با title پیدا کنیم
                try:
                    admin_role = Role.objects.get(title='مدیر کل')
                    if self.user.role != admin_role:
                        self.user.role = admin_role
                        self.user.save(update_fields=['role'])
                except Role.DoesNotExist:
                    logger.warning(f"Role 'مدیر-کل' not found. User {self.user.phone_number} role not updated.")
        
        # Send SMS if is_verified changed from False to True
        if not was_verified and self.is_verified:
            self._send_verification_sms()
    
    def _send_verification_sms(self):
        """Send SMS notification when organizer is verified"""
        try:
            from .sms_service import SMSService
            sms_service = SMSService()
            message = "اشتراک آموزشگاه شما توسط ادمین تایید شد. میتوانید از پنل خود استفاده کنید"
            sms_result = sms_service.send_sms([self.user.phone_number], message)
            
            if not sms_result.get('status'):
                logger.warning(f"Failed to send verification SMS to organizer {self.name} ({self.user.phone_number}): {sms_result.get('error', 'Unknown error')}")
        except Exception as e:
            logger.error(f"Error sending verification SMS to organizer {self.name}: {str(e)}")

    def __str__(self):
        return self.name


class OrganizerTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teachers')
    organization = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='teachers')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone_number


class UserOtp(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    used_count = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField()
    delete_date = models.DateTimeField(null=True, blank=True)

    def generate_otp(self):
        return str(random.randint(10000, 100000))

    def __str__(self):
        return f"{self.phone_number} - {self.code}"


class Role(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Role.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def has_permission(self, permission_slug):
        """بررسی می‌کند که آیا این نقش، یک پرمیژن خاص را دارد یا نه"""
        return self.permissions.filter(permission__slug=permission_slug).exists()

    def __str__(self):
        return self.title


class Permission(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.title:
    #         base_slug = slugify(self.title, allow_unicode=True)
    #         if not self.slug or self.slug != base_slug:
    #             slug = base_slug
    #             counter = 1
    #             while Permission.objects.filter(slug=slug).exclude(id=self.id).exists():
    #                 slug = f'{base_slug}-{counter}'
    #                 counter += 1
    #             self.slug = slug
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        unique_together = ('role', 'permission')  # جلوگیری از ثبت تکراری

    def __str__(self):
        return f"{self.role.title} - {self.permission.title}"


class City(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='cities')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while City.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Province(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Province.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Zone(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='zones')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Zone.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ManualUser(models.Model):
    """Manual user registration - for users registered manually by admins"""
    name = models.CharField(max_length=100, verbose_name='نام')
    lastname = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    nationalcode = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    tel = models.CharField(max_length=11, verbose_name='شماره تلفن')
    birthdate = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    career = models.CharField(max_length=200, blank=True, null=True, verbose_name='شغل')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'کاربر دستی'
        verbose_name_plural = 'کاربران دستی'
        ordering = ['-create_date']

    def __str__(self):
        return f"{self.name} {self.lastname} - {self.nationalcode}"