import secrets
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from account.models import User
from course.models import Course


class Status(models.Model):
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
                while Status.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - User: {self.user.phone_number} - Status: {self.status.title}"


class CourseOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='course_orders')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='course_orders')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    final_price = models.PositiveIntegerField()  # price - discount
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CourseOrder - Course: {self.course.title} - Order ID: {self.order.id}"


class Situation(models.Model):
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
                while Situation.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PaymentGateway(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_sandbox = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)  # Store gateway-specific config
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


class Transaction(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='transactions')
    gateway = models.ForeignKey('PaymentGateway', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    situation = models.ForeignKey('Situation', on_delete=models.CASCADE, related_name='transactions')
    ref_number = models.CharField(max_length=100, unique=True)
    gateway_transaction_id = models.CharField(max_length=100, null=True, blank=True)  # Gateway's transaction ID
    authority = models.CharField(max_length=100, null=True, blank=True)  # For Zarinpal
    payment_url = models.URLField(null=True, blank=True)  # Gateway payment URL
    price = models.PositiveIntegerField()
    card_mask = models.CharField(max_length=100, null=True, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)  # Store gateway response
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.ref_number} for Order {self.order.id}"


class PurchaseCode(models.Model):
    """
    Purchase codes that organizations can buy for courses.
    Normal users can redeem these codes to purchase courses.
    """
    code = models.CharField(max_length=50, unique=True, db_index=True)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='purchase_codes')
    organization = models.ForeignKey('account.Organizer', on_delete=models.CASCADE, related_name='purchase_codes')
    purchased_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='purchased_codes', 
                                     help_text='The organization user who purchased this code')
    total_credits = models.PositiveIntegerField(default=1, help_text='Total number of uses available')
    remaining_credits = models.PositiveIntegerField(default=1, help_text='Remaining number of uses')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Optional expiration date')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['organization', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate unique code
            while True:
                code = secrets.token_urlsafe(16).upper()[:16]  # 16 character code
                if not PurchaseCode.objects.filter(code=code).exists():
                    self.code = code
                    break
        super().save(*args, **kwargs)

    def can_be_used(self):
        """Check if code can be used"""
        if not self.is_active:
            return False, "Code is not active"
        if self.remaining_credits <= 0:
            return False, "Code has no remaining credits"
        if self.expires_at and timezone.now() > self.expires_at:
            return False, "Code has expired"
        return True, None

    def use_credit(self):
        """Use one credit from the code"""
        if self.remaining_credits > 0:
            self.remaining_credits -= 1
            self.save()
            return True
        return False

    def __str__(self):
        return f"Code: {self.code} - Course: {self.course.title} - Credits: {self.remaining_credits}/{self.total_credits}"


class CodeRedemption(models.Model):
    """
    Track when a code is redeemed by a user
    """
    code = models.ForeignKey('PurchaseCode', on_delete=models.CASCADE, related_name='redemptions')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='code_redemptions')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='code_redemptions')
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-redeemed_at']
        unique_together = ('code', 'user', 'course')

    def __str__(self):
        return f"User {self.user.phone_number} redeemed code {self.code.code} for {self.course.title}"
