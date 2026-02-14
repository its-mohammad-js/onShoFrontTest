from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class StaticContent(models.Model):
    CATEGORY_CHOICES = [
        ('skills', 'مهارت ها'),
        ('programs', 'برنامه ها'),
        ('industries', 'صنایع و حرفه ها'),
        ('centers', 'مراکز تخصصی'),
        ('learners', 'مهارت‌آموزان'),
        ('institutes', 'آموزشگاه‌ها'),
        ('onsho', 'آن‌شو'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    short_description = RichTextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل', blank=True, null=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, null=True, max_length=255, verbose_name='اسلاگ')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='onsho',
        verbose_name='دسته بندی'
    )
    display_order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title, allow_unicode=True)
            if not self.slug or self.slug != base_slug:
                slug = base_slug
                counter = 1
                while StaticContent.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'محتوای استاتیک'
        verbose_name_plural = 'محتوای استاتیک'
        ordering = ['category', 'display_order', '-create_date']

    def __str__(self):
        return self.title


class RelatedLink(models.Model):
    static_content = models.ForeignKey(
        StaticContent,
        on_delete=models.CASCADE,
        related_name='related_links',
        verbose_name='محتوای استاتیک'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    url = models.URLField(max_length=500, verbose_name='لینک')
    external = models.BooleanField(default=False, verbose_name='لینک خارجی')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'لینک مرتبط'
        verbose_name_plural = 'لینک‌های مرتبط'
        ordering = ['order', 'create_date']

    def __str__(self):
        return f"{self.title} - {self.static_content.title}"
