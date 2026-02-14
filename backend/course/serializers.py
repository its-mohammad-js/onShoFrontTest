from django.db.models import Avg
from django.utils.timezone import now
from rest_framework import serializers

from account.models import Organizer
from account.models import User
from . import models


def human_readable_time_difference(value):
    if not value:
        return ""

    delta = now() - value
    seconds = delta.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7
    months = days // 30
    years = days // 365

    if seconds < 60:
        return f"{int(seconds)} ثانیه پیش"
    elif minutes < 60:
        return f"{int(minutes)} دقیقه پیش"
    elif hours < 24:
        return f"{int(hours)} ساعت پیش"
    elif days < 7:
        return f"{int(days)} روز پیش"
    elif weeks < 4:
        remaining_days = int(days % 7)
        return f"{int(weeks)} هفته و {remaining_days} روز پیش" if remaining_days > 0 else f"{int(weeks)} هفته پیش"
    elif months < 12:
        remaining_days = int(days % 30)
        return f"{int(months)} ماه و {remaining_days} روز پیش" if remaining_days > 0 else f"{int(months)} ماه پیش"
    else:
        remaining_months = int(months % 12)
        return f"{int(years)} سال و {remaining_months} ماه پیش" if remaining_months > 0 else f"{int(years)} سال پیش"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'phone_number']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeValue
        fields = ['value']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = ['title', 'id', 'slug']


class CourseAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = models.CourseAttribute
        fields = ['attribute', 'value']


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'name', 'logo', 'description', 'slug', 'website_url', 'subdomain']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'title', 'slug', 'parent', 'logo', 'home_page', 'display_order']


class OrganizerListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'name', 'logo', 'slug', 'website_url', 'subdomain']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    organizer = OrganizerListCourseSerializer()
    standard = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    modares = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display', read_only=True)
    type_value = serializers.CharField(source='type', read_only=True)

    class Meta:
        model = models.Course
        fields = [
            'title', 'id', 'excerpt', 'description', 'price', 'discount', 'modares', 'category', 'organizer',
            'standard', 'slug', 'image', 'create_date', 'update_date', 'attributes', 'type', 'type_value',
            'is_popular', 'is_trending'
        ]
    
    def get_standard(self, obj):
        if obj.standard:
            return {
                'id': obj.standard.id,
                'number': obj.standard.number,
                'standard_name': obj.standard.standard_name,
                'cluster': obj.standard.cluster,
                'group_name': obj.standard.group_name,
                'slug': obj.standard.slug
            }
        return None

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_attributes(self, obj):
        # استفاده از related_name برای دریافت ویژگی‌ها
        attributes = obj.course_attributes.all()  # 'course_attributes' همان related_name است که در مدل Course تعریف شده
        result = []
        for attr in attributes:
            result.append({
                "title": attr.attribute.title,
                "id": attr.attribute.id,
                "slug": attr.attribute.slug,
                "value": attr.value
                # به جای custom_value از value در CourseAttribute استفاده می‌شود
            })
        return result

    def get_modares(self, obj):
        # اطلاعات استاد را از مدل user می‌گیریم
        modares = obj.user
        return {
            "first_name": modares.first_name,
            "last_name": modares.last_name,
            "id": modares.id,
            "phone_number": modares.phone_number
        }


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ['file', 'slug', 'id', 'create_date', 'update_date']


# سریالایزر برای درس‌ها
class LessonSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)  # اضافه کردن فایل‌ها به هر درس
    chapter = 'ChapterSerializer'
    description = serializers.CharField(source='content', read_only=True)  # alias برای content
    order = serializers.SerializerMethodField()  # ترتیب درس در فصل

    class Meta:
        model = models.Lesson
        fields = ['title', 'content', 'description', 'slug', 'id', 'create_date', 'update_date', 'published_date', 'is_published', 'is_verified', 'video_link', 'files',
                  'chapter', 'order']  # اضافه کردن چپتر و فایل‌ها
    
    def get_order(self, obj):
        # اگر lesson در یک chapter است، ترتیب آن در chapter را برگردان
        if obj.chapter:
            # محاسبه ترتیب بر اساس create_date در همان chapter
            lessons_in_chapter = models.Lesson.objects.filter(chapter=obj.chapter).order_by('create_date')
            for index, lesson in enumerate(lessons_in_chapter, start=1):
                if lesson.id == obj.id:
                    return index
        # اگر chapter ندارد، ترتیب بر اساس create_date در course
        lessons_in_course = models.Lesson.objects.filter(course=obj.course, chapter__isnull=True).order_by('create_date')
        for index, lesson in enumerate(lessons_in_course, start=1):
            if lesson.id == obj.id:
                return index
        return 1  # پیش‌فرض


# سریالایزر برای چپترها
class ChapterSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()  # فقط درس‌های منتشرشده و تاییدشده

    class Meta:
        model = models.Chapter
        fields = ['title', 'id', 'slug', 'lessons', 'order', 'create_date', 'update_date', ]

    def get_lessons(self, obj):
        queryset = obj.lessons.filter(is_published=True, is_verified=True).order_by('create_date')
        return LessonSerializer(queryset, many=True, context=self.context).data


class TeacherChapterSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()  # همه درس‌ها برای مدرس (تایید شده و نشده)

    class Meta:
        model = models.Chapter
        fields = ['title', 'id', 'slug', 'lessons', 'order', 'create_date', 'update_date', ]

    def get_lessons(self, obj):
        queryset = obj.lessons.all().order_by('create_date')  # همه درس‌ها بدون فیلتر
        return LessonSerializer(queryset, many=True, context=self.context).data


class PublicChapterSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()  # همه درس‌ها برای نمایش عمومی (شامل تایید نشده)

    class Meta:
        model = models.Chapter
        fields = ['title', 'id', 'slug', 'lessons', 'order', 'create_date', 'update_date', ]

    def get_lessons(self, obj):
        queryset = obj.lessons.all().order_by('create_date')  # همه درس‌ها برای نمایش عمومی
        return LessonSerializer(queryset, many=True, context=self.context).data


class UserCommentSerializer:
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_image']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    human_readable_date = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['content', 'user', 'rate', 'create_date', 'human_readable_date']

    def get_user(self, obj):
        # برگرداندن مشخصات کامل کاربر
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "phone_number": obj.user.phone_number,
        }

    def get_rate(self, obj):
        # جستجوی ریتی که کاربر برای این دوره داده است
        rate = models.Rate.objects.filter(user=obj.user, course=obj.course).first()
        if rate:
            return rate.rate
        return None

    def get_human_readable_date(self, obj):
        return human_readable_time_difference(obj.create_date)


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    standard = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    # lessons = LessonSerializer(many=True, read_only=True)
    organizer = OrganizerListCourseSerializer()
    modares = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display', read_only=True)
    type_value = serializers.CharField(source='type', read_only=True)

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'slug', 'excerpt', 'description', 'price', 'discount', 'category',
                  'standard', 'attributes', 'comments', 'chapters', 'image', 'organizer', 'modares', 'average_rate', 'create_date',
                  'update_date', 'type', 'type_value', 'is_popular', 'is_trending']
    
    def get_standard(self, obj):
        if obj.standard:
            return {
                'id': obj.standard.id,
                'number': obj.standard.number,
                'standard_name': obj.standard.standard_name,
                'cluster': obj.standard.cluster,
                'group_name': obj.standard.group_name,
                'slug': obj.standard.slug
            }
        return None

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_attributes(self, obj):
        attributes = models.CourseAttribute.objects.filter(course=obj).select_related('attribute')
        return [{'title': attr.attribute.title, 'value': attr.value} for attr in attributes]

    def get_modares(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'user_image': obj.user.user_image.url if obj.user.user_image else None
        }

    def get_average_rate(self, obj):
        comments = models.Comment.objects.filter(course=obj)
        if comments.exists():
            return round(sum(comment.rate for comment in comments) / comments.count(), 1)
        return 0


class TeacherCourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    standard = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    organizer = OrganizerListCourseSerializer()
    modares = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    chapters = TeacherChapterSerializer(many=True, read_only=True)  # استفاده از TeacherChapterSerializer
    image = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display', read_only=True)
    type_value = serializers.CharField(source='type', read_only=True)

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'slug', 'excerpt', 'description', 'price', 'discount', 'category',
                  'standard', 'attributes', 'comments', 'chapters', 'image', 'organizer', 'modares', 'average_rate', 'create_date',
                  'update_date', 'type', 'type_value', 'is_popular', 'is_trending']
    
    def get_standard(self, obj):
        if obj.standard:
            return {
                'id': obj.standard.id,
                'number': obj.standard.number,
                'standard_name': obj.standard.standard_name,
                'cluster': obj.standard.cluster,
                'group_name': obj.standard.group_name,
                'slug': obj.standard.slug
            }
        return None

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_attributes(self, obj):
        attributes = models.CourseAttribute.objects.filter(course=obj).select_related('attribute')
        return [{'title': attr.attribute.title, 'value': attr.value} for attr in attributes]

    def get_modares(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'user_image': obj.user.user_image.url if obj.user.user_image else None
        }

    def get_average_rate(self, obj):
        comments = models.Comment.objects.filter(course=obj)
        if comments.exists():
            return round(sum(comment.rate for comment in comments) / comments.count(), 1)
        return 0


class PublicCourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    standard = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    organizer = OrganizerListCourseSerializer()
    modares = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    chapters = PublicChapterSerializer(many=True, read_only=True)  # استفاده از PublicChapterSerializer
    image = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display', read_only=True)
    type_value = serializers.CharField(source='type', read_only=True)

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'slug', 'excerpt', 'description', 'price', 'discount', 'category',
                  'standard', 'attributes', 'comments', 'chapters', 'image', 'organizer', 'modares', 'average_rate', 'create_date',
                  'update_date', 'type', 'type_value', 'is_popular', 'is_trending']
    
    def get_standard(self, obj):
        if obj.standard:
            return {
                'id': obj.standard.id,
                'number': obj.standard.number,
                'standard_name': obj.standard.standard_name,
                'cluster': obj.standard.cluster,
                'group_name': obj.standard.group_name,
                'slug': obj.standard.slug
            }
        return None

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_attributes(self, obj):
        attributes = models.CourseAttribute.objects.filter(course=obj).select_related('attribute')
        return [{'title': attr.attribute.title, 'value': attr.value} for attr in attributes]

    def get_modares(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'user_image': obj.user.user_image.url if obj.user.user_image else None
        }

    def get_average_rate(self, obj):
        comments = models.Comment.objects.filter(course=obj)
        if comments.exists():
            return round(sum(comment.rate for comment in comments) / comments.count(), 1)
        return 0

    def get_attributes(self, obj):
        attributes = models.CourseAttribute.objects.filter(course=obj).select_related('attribute')
        return [{'title': attr.attribute.title, 'value': attr.value} for attr in attributes]

    def get_modares(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'user_image': obj.user.user_image.url if obj.user.user_image else None
        }

    def get_average_rate(self, obj):
        comments = models.Comment.objects.filter(course=obj)
        if comments.exists():
            return round(sum(comment.rate for comment in comments) / comments.count(), 1)
        return 0
        for attr in attributes:
            result.append({
                "title": attr.attribute.title,
                "id": attr.attribute.id,
                "slug": attr.attribute.slug,
                "value": attr.value
                # به جای custom_value از value در CourseAttribute استفاده می‌شود
            })
        return result

    def get_average_rate(self, obj):
        # محاسبه میانگین ریت برای دوره
        rates = obj.rates.all()
        if rates.exists():
            return round(rates.aggregate(Avg('rate'))['rate__avg'], 2)
        return None


# ------------------------------------------------------------------------------------------------------------------------
# this is for category list

class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'logo', 'slug', 'children', 'home_page']

    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return RecursiveCategorySerializer(children, context=self.context, many=True).data
        return None

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None


# ------------------------------------------------------------------------------------------------------------------------
# this is for creating comment and rate

class CommentCreateSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ('course', 'content', 'rate')

    def get_rate(self, obj):
        user = self.context['request'].user
        course = obj.course

        # Check if the user has rated this course
        rate = models.Rate.objects.filter(user=user, course=course).first()
        if rate:
            return rate.rate
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


# ------------------------------------------------------------------------------------------------------------------------
# this is for create, remove and list the wishlists

class CreateRemoveWishListSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)

    def validate_course_id(self, value):
        # بررسی اینکه آیا آگهی با این ID وجود دارد
        if not models.Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("دوره مورد نظر یافت نشد.")
        return value


# ------------------------------------------------------------------------------------------------------------------------
# this is for create and update task

class TaskSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta:
        model = models.Task
        fields = ['id', 'title', 'description', 'mentor', 'course', 'lesson', 'file', 'difficulty', 'time_limit', 'slug']

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_course(self, obj):
        if obj.course:
            return {
                'id': obj.course.id,
                'title': obj.course.title,
                'slug': obj.course.slug
            }
        return None

    def update(self, instance, validated_data):
        # Handle file upload
        if 'file' in self.context.get('request').FILES:
            instance.file = self.context.get('request').FILES['file']
        return super().update(instance, validated_data)


# ------------------------------------------------------------------------------------------------------------------------
# this is for create and update onrganization

class CreateOrganizerSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Organizer
        fields = ['id', 'name', 'logo', 'description', 'slug', 'website_url', 'subdomain', 'is_active', 'is_verified']
        read_only_fields = ['slug', 'is_active', 'is_verified']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.logo and request:
            representation['logo'] = request.build_absolute_uri(instance.logo.url)
        return representation


# ------------------------------------------------------------------------------------------------------------------------
# create and update course, chapter and lesson by mohammad

class UserOrganizeSerializer(serializers.ModelSerializer):
    # استفاده از Serializer برای نمایش اطلاعات Organizer
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'gender', 'birthday', 'age', 'user_image',
                  'organizer']


class CourseCreateSerializer(serializers.ModelSerializer):
    attributes = CourseAttributeSerializer(many=True, write_only=True, required=False)
    user = UserOrganizeSerializer(read_only=True)
    old_standard_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'excerpt', 'description', 'price', 'discount', 'category', 'organizer', 'mentor',
                  'standard', 'image', 'slug', 'type', 'is_popular', 'is_trending',
                  'attributes', 'user', 'old_standard_code']

    def create(self, validated_data):
        # استخراج داده‌های attributes از داده‌های ورودی
        attributes_data = validated_data.pop('attributes', [])
        validated_data['user'] = self.context['request'].user  # تنظیم کاربر به عنوان کاربر وارد شده
        
        # category و mentor ممکن است read_only باشند، پس باید از initial_data بگیریم
        category_id = self.initial_data.get('category')
        mentor_id = self.initial_data.get('mentor')
        
        if category_id:
            try:
                validated_data['category'] = models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                pass
        
        if mentor_id:
            try:
                validated_data['mentor'] = User.objects.get(id=mentor_id)
            except User.DoesNotExist:
                pass

        # ایجاد دوره جدید
        course = models.Course.objects.create(**validated_data)

        # ایجاد ویژگی‌ها برای دوره
        for attr_data in attributes_data:
            # بررسی درست بودن فرمت داده‌ها
            attribute = attr_data['attribute']
            value = attr_data.get('value')

            # ایجاد ویژگی‌های دوره
            models.CourseAttribute.objects.create(
                course=course,
                attribute=attribute,
                value=value
            )

        return course

    def update(self, instance, validated_data):
        # استخراج داده‌های attributes برای به‌روزرسانی
        attributes_data = validated_data.pop('attributes', [])
        
        # حذف فیلدهایی که نباید در ویرایش تغییر کنند
        # این فیلدها فقط در زمان ایجاد قابل تنظیم هستند
        validated_data.pop('category', None)  # دسته بندی قابل تغییر نیست
        validated_data.pop('mentor', None)  # منتور قابل تغییر نیست

        # به‌روزرسانی سایر فیلدهای دوره
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # به‌روزرسانی ویژگی‌ها
        # فیلدهایی که نباید در ویرایش تغییر کنند
        restricted_attributes = ['پیش‌نیاز', 'زبان آموزش', 'زبان']
        
        for attr_data in attributes_data:
            attribute_id = attr_data['attribute']
            value = attr_data.get('value')
            
            # بررسی اینکه آیا این attribute در لیست محدود شده‌ها است
            try:
                attribute = models.Attribute.objects.get(id=attribute_id)
                if attribute.title in restricted_attributes:
                    # این attribute قابل تغییر نیست - از به‌روزرسانی صرف نظر می‌کنیم
                    continue
            except models.Attribute.DoesNotExist:
                pass

            # به‌روزرسانی یا ایجاد ویژگی‌های دوره
            models.CourseAttribute.objects.update_or_create(
                course=instance,
                attribute_id=attribute_id,
                defaults={'value': value}
            )

        return instance

    def to_representation(self, instance):
        """سفارشی کردن نحوه نمایش اطلاعات دوره"""
        representation = super().to_representation(instance)
        attributes = models.CourseAttribute.objects.filter(course=instance)
        representation['attributes'] = CourseAttributeSerializer(attributes, many=True).data
        return representation


class ChapterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['title', 'course', 'order', 'id']

    def validate_course(self, value):
        # بررسی اینکه آیا کورس متعلق به کاربر است
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("You do not have permission to add a chapter to this course.")

        # بررسی اینکه نقش کاربر "استاد" یا "مدیر-کل" است
        if user.role.slug not in ['استاد', 'مدیر-کل']:
            raise serializers.ValidationError("You must be a mentor or super admin to add a chapter.")

        return value

    def update(self, instance, validated_data):
        # بروزرسانی فیلدهای چپتر
        instance.title = validated_data.get('title', instance.title)
        instance.order = validated_data.get('order', instance.order)
        instance.course = validated_data.get('course', instance.course)

        instance.save()
        return instance


class LessonCreateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),  # فایل‌های ارسال‌شده
        write_only=True,
        required=False
    )
    uploaded_files = serializers.SerializerMethodField()  # فیلد فقط خواندنی برای نمایش فایل‌ها
    chapter = ChapterSerializer

    class Meta:
        model = models.Lesson
        fields = ['title', 'id', 'content', 'course', 'chapter', 'video_link', 'files', 'uploaded_files', 'published_date', 'is_published', 'is_verified',
                  'create_date', 'update_date']

    def get_uploaded_files(self, obj):
        request = self.context.get('request')  # درخواست از کانتکست دریافت می‌شود
        files = models.File.objects.filter(lesson=obj)
        return [
            {
                "id": file.id,
                "file": request.build_absolute_uri(file.file.url) if request else file.file.url,
                "create_date": file.create_date.isoformat() if file.create_date else None,
                "update_date": file.update_date.isoformat() if file.update_date else None,
            }
            for file in files
        ]

    def validate_course(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("You do not have permission to add a lesson to this course.")
        return value

    def create(self, validated_data):
        # جدا کردن داده‌های فایل‌ها
        files_data = validated_data.pop('files', [])
        # New lessons start unpublished and unverified
        validated_data['is_published'] = False
        validated_data['is_verified'] = False
        lesson = models.Lesson.objects.create(**validated_data)

        # ذخیره فایل‌ها
        for file in files_data:
            models.File.objects.create(
                file=file,
                lesson=lesson,
                user=self.context['request'].user
            )

        # ایجاد جلسات (Session) برای تمام کاربران ثبت‌نام‌شده در دوره
        course_users = models.CourseUser.objects.filter(course=lesson.course)
        for course_user in course_users:
            models.Session.objects.create(
                lesson=lesson,
                user=course_user.user,
                step=models.Step.objects.first()  # یا هر مرحله پیش‌فرض دیگری
            )

        return lesson


class LessonUpdateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),  # فایل‌های ارسال‌شده
        write_only=True,
        required=False
    )
    uploaded_files = serializers.SerializerMethodField()  # فیلد فقط خواندنی برای نمایش فایل‌ها

    class Meta:
        model = models.Lesson
        fields = ['title', 'content', 'course', 'chapter', 'files', 'uploaded_files']

    def get_uploaded_files(self, obj):
        """
        بازگرداندن فایل‌های مرتبط با درس به همراه زمان ایجاد و آخرین به‌روزرسانی.
        """
        request = self.context.get('request')  # درخواست از کانتکست دریافت می‌شود
        files = models.File.objects.filter(lesson=obj)
        return [
            {
                "id": file.id,
                "file": request.build_absolute_uri(file.file.url) if request else file.file.url,
                "create_date": file.create_date.isoformat() if file.create_date else None,
                "update_date": file.update_date.isoformat() if file.update_date else None,
            }
            for file in files
        ]

    def validate_course(self, value):
        """
        بررسی اینکه آیا کاربر اجازه ویرایش این درس را دارد.
        """
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("You do not have permission to edit this course.")
        return value

    def update(self, instance, validated_data):
        """
        به‌روزرسانی درس و فایل‌های مرتبط.
        """
        # جدا کردن فایل‌ها از داده‌های معتبر
        files_data = validated_data.pop('files', [])

        # به‌روزرسانی سایر فیلدهای درس
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # اضافه کردن فایل‌های جدید
        for file in files_data:
            models.File.objects.create(
                file=file,
                lesson=instance,
                user=self.context['request'].user
            )

        return instance


# ------------------------------------------------------------------------------------------------------------------------
# this is for user course list

class CourseUserSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.CourseUser
        fields = '__all__'  # شامل تمام فیلدهای مدل
        read_only_fields = ('create_date', 'update_date')

    def validate_status(self, value):
        """
        اعتبارسنجی مقدار فیلد وضعیت.
        """
        valid_statuses = [choice[0] for choice in models.CourseUser.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError("وضعیت انتخابی معتبر نیست.")
        return value


# ------------------------------------------------------------------------------------------------------------------------
# this is for attribute list

class AttributeListSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()

    class Meta:
        model = models.Attribute
        fields = ['title', 'id', 'slug', 'type', 'values']

    def get_values(self, obj):
        return [value.value for value in obj.values.all()]


# -----------------------------------------------------------------------------------------------------------------------
# this is for OrganizationsList

class OrganizationListSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    course_types = serializers.SerializerMethodField()

    class Meta:
        model = Organizer
        fields = ['id', 'name', 'logo', 'description', 'slug', 'website_url', 'subdomain', 'is_active', 'is_verified', 'course_types', 'create_date', 'update_date']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None
    
    def get_course_types(self, obj):
        """
        بازگرداندن array از TYPE_CHOICES دوره‌های فعال این آموزشگاه
        """
        from course.models import Course
        # دریافت تمام دوره‌های این آموزشگاه
        courses = Course.objects.filter(organizer=obj).values_list('type', flat=True).distinct()
        
        # تبدیل به array از TYPE_CHOICES
        TYPE_CHOICES = [
            ('offline', 'آفلاین'),
            ('online', 'آنلاین'),
            ('pre_registration', 'پیش ثبت نام حضوری'),
        ]
        
        # ساخت dictionary برای دسترسی سریع
        type_dict = dict(TYPE_CHOICES)
        
        # ساخت array از type های موجود
        result = []
        for course_type in courses:
            if course_type in type_dict:
                result.append({
                    'value': course_type,
                    'label': type_dict[course_type]
                })
        
        return result


# ------------------------------------------------------------------------------------------------------------------------
# this is for create taskanswer

class TaskAnswerSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = models.TaskAnswer
        fields = ['id', 'user', 'file', 'description', 'deadline', 'status', 'create_date', 'update_date']

    def get_file(self, obj):
        request = self.context.get('request', None)  # بررسی مقدار request
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url
        return None


# ------------------------------------------------------------------------------------------------------------------------
# this if for taskdetail

class TaskDetailSerializer(serializers.ModelSerializer):
    answers = TaskAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Task
        fields = ['id', 'title', 'description', 'mentor', 'lesson', 'file', 'difficulty', 'slug', 'create_date',
                  'update_date', 'answers']


# ------------------------------------------------------------------------------------------------------------------------
# this if for answerlist

class TaskSummarySerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = models.Task
        fields = ["id", "title", "description", "difficulty", "file", "create_date"]

    def get_file(self, obj):
        request = self.context.get('request', None)  # بررسی مقدار request
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url
        return None


class AnswerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    task = TaskSummarySerializer()

    class Meta:
        model = models.TaskAnswer
        fields = ["id", "user", "task", "file", "description", "deadline", "status", "create_date", "update_date"]


# ------------------------------------------------------------------------------------------------------------------------
# Standards serializers

class StandardsSerializer(serializers.ModelSerializer):
    """Basic serializer for Standards model"""
    level = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Standards
        fields = [
            'id', 'number', 'cluster', 'group_name', 'standard_name', 'standard_name_latin',
            'old_standard_code', 'version', 'competency_code', 'isco_job_code', 'isco_group_code',
            'entry_education_level', 'theoretical_hours', 'practical_hours', 'internship_hours',
            'project_hours', 'total_hours', 'work_and_knowledge', 'type', 'compilation_date',
            'parent', 'level', 'slug', 'create_date', 'update_date'
        ]


class RecursiveStandardsSerializer(serializers.ModelSerializer):
    """Recursive serializer for tree structure of Standards"""
    children = serializers.SerializerMethodField()
    level = serializers.ReadOnlyField()
    
    class Meta:
        model = models.Standards
        fields = [
            'id', 'number', 'cluster', 'group_name', 'standard_name', 'standard_name_latin',
            'old_standard_code', 'version', 'competency_code', 'isco_job_code', 'isco_group_code',
            'entry_education_level', 'theoretical_hours', 'practical_hours', 'internship_hours',
            'project_hours', 'total_hours', 'work_and_knowledge', 'type', 'compilation_date',
            'parent', 'level', 'slug', 'create_date', 'update_date', 'children'
        ]
    
    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return RecursiveStandardsSerializer(children, context=self.context, many=True).data
        return []


class StandardsListSerializer(serializers.ModelSerializer):
    """Serializer for listing standards with basic information"""
    level = serializers.ReadOnlyField()
    parent_name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Standards
        fields = [
            'id', 'number', 'standard_name', 'cluster', 'group_name', 'parent', 'parent_name',
            'level', 'total_hours', 'type', 'compilation_date', 'slug', 'old_standard_code'
        ]
    
    def get_parent_name(self, obj):
        if obj.parent:
            return obj.parent.standard_name
        return None


class StandardsCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating standards"""
    
    class Meta:
        model = models.Standards
        fields = [
            'number', 'cluster', 'group_name', 'standard_name', 'standard_name_latin',
            'old_standard_code', 'version', 'competency_code', 'isco_job_code', 'isco_group_code',
            'entry_education_level', 'theoretical_hours', 'practical_hours', 'internship_hours',
            'project_hours', 'total_hours', 'work_and_knowledge', 'type', 'compilation_date', 'parent'
        ]
    
    def validate(self, data):
        # Validate that total_hours equals sum of other hours (only if all are provided)
        theoretical = data.get('theoretical_hours', 0) or 0
        practical = data.get('practical_hours', 0) or 0
        internship = data.get('internship_hours', 0) or 0
        project = data.get('project_hours', 0) or 0
        total = data.get('total_hours', 0) or 0
        
        # Only validate if at least one hour field is provided
        if any([theoretical, practical, internship, project, total]):
            calculated_total = theoretical + practical + internship + project
            if total != calculated_total:
                raise serializers.ValidationError(
                    f"مجموع ساعات باید برابر با ساعت کل باشد. مجموع محاسبه شده: {calculated_total}"
                )
        
        return data


class StandardsDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for standards with related data"""
    level = serializers.ReadOnlyField()
    parent_info = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()
    ancestors = serializers.SerializerMethodField()
    siblings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Standards
        fields = [
            'id', 'number', 'cluster', 'group_name', 'standard_name', 'standard_name_latin',
            'old_standard_code', 'version', 'competency_code', 'isco_job_code', 'isco_group_code',
            'entry_education_level', 'theoretical_hours', 'practical_hours', 'internship_hours',
            'project_hours', 'total_hours', 'work_and_knowledge', 'type', 'compilation_date',
            'parent', 'level', 'slug', 'create_date', 'update_date', 'parent_info', 
            'children_count', 'ancestors', 'siblings_count'
        ]
    
    def get_parent_info(self, obj):
        if obj.parent:
            return {
                'id': obj.parent.id,
                'number': obj.parent.number,
                'standard_name': obj.parent.standard_name,
                'slug': obj.parent.slug
            }
        return None
    
    def get_children_count(self, obj):
        return obj.children.count()
    
    def get_ancestors(self, obj):
        ancestors = obj.get_ancestors()
        return [
            {
                'id': ancestor.id,
                'number': ancestor.number,
                'standard_name': ancestor.standard_name,
                'slug': ancestor.slug
            }
            for ancestor in ancestors
        ]
    
    def get_siblings_count(self, obj):
        return obj.get_siblings().count()