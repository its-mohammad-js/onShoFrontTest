from rest_framework import serializers

from course.models import Course
from course.serializers import CourseSerializer
from .models import Status, Order, CourseOrder, PurchaseCode, CodeRedemption


class CourseOrderSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()  # تغییر از course به course_id
    quantity = serializers.IntegerField(default=1)



class OrderCreateSerializer(serializers.Serializer):
    courses = CourseOrderSerializer(many=True)
    user_info = serializers.DictField(required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        courses_data = validated_data.pop('courses')
        user_info = validated_data.get('user_info', {})

        # Update user info
        for field, value in user_info.items():
            setattr(user, field, value)
        user.save()

        # Get or create default pending status
        status_obj, created = Status.objects.get_or_create(slug='pending', defaults={'title': 'Pending'})

        # بررسی خرید قبلی
        purchased_courses = Order.objects.filter(user=user).values_list('course_orders__course_id', flat=True)
        invalid_courses = [
            course_data['course_id']
            for course_data in courses_data
            if course_data['course_id'] in purchased_courses
        ]

        if invalid_courses:
            raise serializers.ValidationError({
                "courses": f"Course(s) with ID(s) {', '.join(map(str, invalid_courses))} already purchased."
            })

        # Create Order
        order = Order.objects.create(user=user, status=status_obj, total_price=0)  # مقدار اولیه 0

        total_price = 0

        for course_data in courses_data:
            course = Course.objects.get(id=course_data['course_id'])
            quantity = course_data['quantity']
            price = course.price
            discount = course.discount or 0
            final_price = price - discount
            total_price += final_price * quantity

            # Create CourseOrder
            CourseOrder.objects.create(
                order=order,
                course=course,
                quantity=quantity,
                price=price,
                discount=discount,
                final_price=final_price
            )

        # Update total price in the order
        order.total_price = total_price
        order.save()  # مقدار total_price ذخیره می‌شود

        return order


class PurchaseCodeCreateSerializer(serializers.Serializer):
    """Serializer for organization users to buy courses and generate codes"""
    course_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, default=1, 
                                         help_text='Number of codes to generate (credits per code)')
    credits_per_code = serializers.IntegerField(min_value=1, default=1,
                                                  help_text='Number of uses (credits) per code')

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")
        return value


class PurchaseCodeSerializer(serializers.ModelSerializer):
    """Serializer for displaying purchase codes"""
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(source='course.id', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = PurchaseCode
        fields = ['id', 'code', 'course', 'course_id', 'organization_name', 
                  'total_credits', 'remaining_credits', 'is_active', 
                  'expires_at', 'create_date']
        read_only_fields = ['code', 'total_credits', 'remaining_credits', 
                           'is_active', 'create_date']


class CodeRedeemSerializer(serializers.Serializer):
    """Serializer for normal users to redeem codes"""
    code = serializers.CharField(max_length=50, required=True)

    def validate_code(self, value):
        try:
            purchase_code = PurchaseCode.objects.get(code=value.upper())
        except PurchaseCode.DoesNotExist:
            raise serializers.ValidationError("Invalid code")
        
        can_use, error_message = purchase_code.can_be_used()
        if not can_use:
            raise serializers.ValidationError(error_message)
        
        return value.upper()


class CodeRedemptionSerializer(serializers.ModelSerializer):
    """Serializer for displaying code redemptions"""
    code = serializers.CharField(source='code.code', read_only=True)
    course = CourseSerializer(read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = CodeRedemption
        fields = ['id', 'code', 'course', 'user_phone', 'redeemed_at']
        read_only_fields = ['redeemed_at']

