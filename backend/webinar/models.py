from django.db import models


class Webinar(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان وبینار")
    description = models.TextField(verbose_name="توضیحات وبینار")
    speaker = models.CharField(max_length=255, verbose_name="سخنران")
    date = models.CharField(max_length=150, verbose_name="تاریخ وبینار")
    start_time = models.TimeField(verbose_name="زمان شروع")
    end_time = models.TimeField(verbose_name="زمان پایان")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    is_free = models.BooleanField(default=False, verbose_name="رایگان")
    image = models.ImageField(upload_to="webinars/", verbose_name="تصویر وبینار", null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    update_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "وبینار"
        verbose_name_plural = "وبینارها"
        ordering = ["-date", "start_time"]


class WebinarTopic(models.Model):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name="topics", verbose_name="وبینار")
    title = models.CharField(max_length=255, verbose_name="عنوان سرفصل")
    content = models.TextField(verbose_name="محتوای سرفصل")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "سرفصل وبینار"
        verbose_name_plural = "سرفصل‌های وبینار"
