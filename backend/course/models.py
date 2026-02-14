from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from account.models import User, Organizer


class Course(models.Model):
    TYPE_CHOICES = [
        ('offline', 'آفلاین'),
        ('online', 'آنلاین'),
        ('pre_registration', 'پیش ثبت نام حضوری'),
    ]
    
    title = models.CharField(max_length=100)
    excerpt = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='online',
        verbose_name='نوع دوره'
    )
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='courses')
    organizer = models.ForeignKey('account.Organizer', on_delete=models.CASCADE, related_name='courses')
    mentor = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='mentor_courses', blank=True,
                               null=True)
    standard = models.ForeignKey('Standards', on_delete=models.SET_NULL, related_name='courses', blank=True, null=True,
                                verbose_name='استاندارد')
    image = models.ImageField(upload_to='course', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    is_popular = models.BooleanField(
        default=False,
        verbose_name='محبوب ترین',
        help_text='اگر این گزینه را انتخاب کنید، دوره در بخش محبوب ترین نمایش داده خواهد شد'
    )
    is_trending = models.BooleanField(
        default=False,
        verbose_name='ترند',
        help_text='اگر این گزینه را انتخاب کنید، دوره در بخش ترند نمایش داده خواهد شد'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='منتشر شده',
        help_text='دوره فقط زمانی منتشر می‌شود که تایید شده باشد'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='تایید شده',
        help_text='دوره باید توسط ادمین تایید شود تا منتشر شود'
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # اگر دوره موجود است و فیلدهای مهم تغییر کرده‌اند، نیاز به تایید مجدد دارد
        if self.pk is not None:
            try:
                original = Course.objects.get(pk=self.pk)
                # اگر title، excerpt، description یا price تغییر کرده
                if (original.title != self.title or 
                    original.excerpt != self.excerpt or 
                    original.description != self.description or
                    original.price != self.price or
                    original.discount != self.discount):
                    # نیاز به تایید مجدد
                    self.is_verified = False
                    self.is_published = False
            except Course.DoesNotExist:
                pass
        
        # منطق slug
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Course.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        
        # اگر is_verified=False است، is_published هم باید False باشد
        if not self.is_verified:
            self.is_published = False
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseUser(models.Model):
    STATUS_CHOICES = [
        ('completed', 'کامل‌شده'),
        ('in_progress', 'در حال پیشرفت'),
        ('not_started', 'شروع نشده'),
        ('cancelled', 'لغو شده'),
    ]
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='enrolled_courses')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started',
        verbose_name='وضعیت'
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.phone_number} enrolled in {self.course.title}"


class Category(models.Model):
    title = models.CharField(max_length=300)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True, max_length=255)
    logo = models.ImageField(upload_to='category', blank=True, null=True)
    # New fields for mapping to external standard/ISCO codes
    old_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='کد قدیم')
    isco_code = models.CharField(max_length=512, blank=True, null=True, verbose_name='کد ISCO تجمیعی')
    # home_page = models.BooleanField(default=False ,verbose_name='نمایش در صفحه اصلی', help_text='اگر این گزینه رو انتخاب کنید، دسته بندی در صفحه اصلی نمایش داده خواهد شد')
    home_page = models.BooleanField(
        default=False,
        verbose_name='نمایش در صفحه اصلی',
        help_text='اگر این گزینه رو انتخاب کنید، دسته بندی در صفحه اصلی نمایش داده خواهد باشد'
    )
    display_order = models.IntegerField(
        default=9999,
        null=True,
        blank=True,
        verbose_name='اولویت نمایش',
        help_text='عدد کمتر = اولویت بالاتر. دسته‌بندی‌ها بر اساس این فیلد مرتب می‌شوند.'
    )

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=150)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='chapters')
    order = models.PositiveIntegerField(default=0)  # ترتیب نمایش فصل‌ها
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Chapter.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='lessons', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True, help_text="لینک ویدیو درس")
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If existing lesson and content-like fields changed, require re-verification and unpublish
        if self.pk is not None:
            try:
                original = Lesson.objects.get(pk=self.pk)
                if original.title != self.title or original.content != self.content:
                    self.is_verified = False
                    self.is_published = False
            except Lesson.DoesNotExist:
                pass

        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Lesson.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class File(models.Model):
    file = models.FileField(upload_to='files')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='files')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='files')
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.lesson.title:
            base_slug = slugify(self.lesson.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while File.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)


class Attribute(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value


class CourseAttribute(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_attributes')
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='course_attributes')
    value = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class CategoryAttribute(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_attributes')
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='category_attributes')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='comments')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Step(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Step.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Session(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='sessions')
    step = models.ForeignKey('Step', on_delete=models.CASCADE, related_name='sessions')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lesson


class Task(models.Model):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

    DIFFICULT_LEVELS = [
        (BEGINNER, 'مبتدی'),
        (INTERMEDIATE, 'متوسط'),
        (ADVANCED, 'پیشرفته'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    mentor = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='mentor_tasks')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    file = models.FileField(upload_to='tasks/', null=True, blank=True)
    difficulty = models.CharField(max_length=15, choices=DIFFICULT_LEVELS, default=BEGINNER)
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes for answering the task")
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Task.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        
        # Automatically set course from lesson if not set
        if self.lesson and not self.course:
            self.course = self.lesson.course
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TaskAnswer(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='task_answers')
    file = models.FileField(upload_to='task_answers/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey('AnswerStatus', on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.user} for {self.task.title}"


class AnswerStatus(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.title:
    #         base_slug = slugify(self.title, allow_unicode=True)
    #         if not self.slug or self.slug != base_slug:
    #             slug = base_slug
    #             counter = 1
    #             while TaskStatus.objects.filter(slug=slug).exclude(id=self.id).exists():
    #                 slug = f'{base_slug}-{counter}'
    #                 counter += 1
    #             self.slug = slug
    #     super().save(*args, **kwargs)
    #
    # def __str__(self):
    #     return self.title


class Rate(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='rates')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='rates')
    rate = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.course.title} - {self.rate}"


class WishList(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='wishlists')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='wishlists')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.phone_number} -> {self.course.title}"


class Standards(models.Model):
    """
    Standards model with tree structure for vocational training standards
    """
    # Tree structure fields
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', 
                              blank=True, null=True, verbose_name='والد')
    
    # Basic information
    number = models.PositiveIntegerField(blank=True, null=True, verbose_name='شماره')
    cluster = models.CharField(max_length=200, blank=True, null=True, verbose_name='خوشه')
    group_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='نام گروه')
    standard_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='نام استاندارد')
    standard_name_latin = models.CharField(max_length=300, blank=True, null=True, 
                                         verbose_name='نام استاندارد به لاتین')
    
    # Codes
    old_standard_code = models.CharField(max_length=200, blank=True, null=True, verbose_name='کد استاندارد قدیم')
    version = models.PositiveIntegerField(default=1, blank=True, null=True, verbose_name='نسخه')
    competency_code = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='کد شایستگی')
    
    # ISCO fields
    isco_job_code = models.PositiveIntegerField(blank=True, null=True, verbose_name='کد شغل ISCO')
    isco_group_code = models.PositiveIntegerField(blank=True, null=True, verbose_name='کد گروه ISCO')
    
    # Education level
    entry_education_level = models.CharField(max_length=300, blank=True, null=True, verbose_name='سطح تحصیلات ورودی')
    
    # Hours
    theoretical_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name='ساعت نظری')
    practical_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name='ساعت عملی')
    internship_hours = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='ساعت کارورزی')
    project_hours = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='ساعت پروژه')
    total_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name='ساعت کل')
    
    # Additional fields
    work_and_knowledge = models.CharField(max_length=100, default='هیچ کدام', blank=True, null=True,
                                        verbose_name='کارو دانش')
    type = models.CharField(max_length=100, default='شغل', blank=True, null=True, verbose_name='نوع')
    
    # Dates
    compilation_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تدوین و به روز رسانی')
    
    # System fields
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True, max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'استاندارد'
        verbose_name_plural = 'استانداردها'
        ordering = ['number']
    
    def save(self, *args, **kwargs):
        if self.standard_name:
            base_slug = slugify(self.standard_name, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while Standards.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.number} - {self.standard_name}"
    
    @property
    def level(self):
        """Calculate the level in the tree structure"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    
    def get_ancestors(self):
        """Get all ancestors of this standard"""
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors
    
    def get_descendants(self):
        """Get all descendants of this standard"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def get_siblings(self):
        """Get all siblings of this standard"""
        if self.parent:
            return self.parent.children.exclude(id=self.id)
        return Standards.objects.filter(parent__isnull=True).exclude(id=self.id)
