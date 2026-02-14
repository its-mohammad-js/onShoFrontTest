from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'old_code', 'isco_code']
    list_display = ['title', 'parent', 'old_code', 'isco_code', 'home_page', 'display_order', 'create_date', 'update_date']
    list_filter = ['parent', 'home_page']
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('title', 'slug', 'parent', 'logo')
        }),
        ('کدها', {
            'fields': ('old_code', 'isco_code'),
            'description': 'کد قدیم و کد ISCO مرتبط با این دسته‌بندی.'
        }),
        ('نمایش در صفحه اصلی', {
            'fields': ('home_page', 'display_order'),
            'description': 'اولویت نمایش: عدد کمتر = اولویت بالاتر. اگر خالی باشد، مقدار 9999 استفاده می‌شود.'
        }),
    )

@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']


class CourseAttributeInline(admin.TabularInline):
    model = models.CourseAttribute
    extra = 1


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'type', 'is_published', 'is_verified', 'is_popular', 'is_trending', 'user', 'mentor', 'update_date']
    list_filter = ['type', 'is_published', 'is_verified', 'is_popular', 'is_trending', 'create_date', 'update_date']
    inlines = [CourseAttributeInline, ]
    actions = ['verify_and_publish_selected', 'unverify_selected']
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('title', 'excerpt', 'description', 'slug')
        }),
        ('دسته‌بندی و سازمان‌دهی', {
            'fields': ('category', 'organizer', 'user', 'mentor', 'standard', 'type')
        }),
        ('قیمت‌گذاری', {
            'fields': ('price', 'discount')
        }),
        ('وضعیت انتشار و تایید', {
            'fields': ('is_published', 'is_verified'),
            'description': 'دوره باید تایید شود تا منتشر شود. اگر is_verified=False باشد، is_published هم False می‌شود.'
        }),
        ('ویژگی‌های نمایش', {
            'fields': ('is_popular', 'is_trending', 'image')
        }),
        ('تاریخ‌ها', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('create_date', 'update_date')
    
    def verify_and_publish_selected(self, request, queryset):
        """تایید و انتشار دوره‌های انتخاب شده"""
        updated = queryset.update(is_verified=True, is_published=True)
        self.message_user(request, f'{updated} دوره تایید و منتشر شد.')
    verify_and_publish_selected.short_description = 'تایید و انتشار دوره‌های انتخاب شده'
    
    def unverify_selected(self, request, queryset):
        """عدم تایید دوره‌های انتخاب شده (و عدم انتشار)"""
        updated = queryset.update(is_verified=False, is_published=False)
        self.message_user(request, f'{updated} دوره عدم تایید شد و از انتشار خارج شد.')
    unverify_selected.short_description = 'عدم تایید دوره‌های انتخاب شده'


@admin.register(models.Chapter)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['course']
    search_fields = ['title']
    list_display = ['title', 'course']


class FileInline(admin.TabularInline):
    model = models.File
    extra = 1


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = ['course', 'is_published', 'is_verified']
    search_fields = ['title']
    list_display = ['title', 'course', 'is_published', 'is_verified', 'update_date']
    actions = ['publish_selected', 'unpublish_selected', 'verify_selected', 'unverify_selected']

    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = 'Publish selected lessons'

    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = 'Unpublish selected lessons'

    def verify_selected(self, request, queryset):
        queryset.update(is_verified=True)
    verify_selected.short_description = 'Verify selected lessons'

    def unverify_selected(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_selected.short_description = 'Unverify selected lessons'


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'create_date', 'update_date', 'difficulty')
    list_filter = ('lesson', 'create_date', 'update_date', 'difficulty')
    search_fields = ('title', 'description', 'slug')


@admin.register(models.AnswerStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')


@admin.register(models.TaskAnswer)
class TaskAnswerAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'deadline', 'create_date', 'update_date')
    list_filter = ('create_date', 'update_date')
    search_fields = ('task__title', 'user__first_name', 'user__last_name')


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'step', 'start_date', 'end_date', 'create_date', 'update_date')
    list_filter = ('lesson', 'user', 'step', 'start_date', 'end_date')
    search_fields = ('lesson__title', 'user__username', 'step__title')


@admin.register(models.Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rate', 'create_date')
    list_filter = ('rate', 'create_date')
    search_fields = ('user__username', 'course__title')
    ordering = ('-create_date',)


@admin.register(models.CourseUser)
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'create_date')
    list_filter = ('user', 'course', 'status')
    ordering = ('-create_date',)


@admin.register(models.Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'create_date')


@admin.register(models.Standards)
class StandardsAdmin(admin.ModelAdmin):
    list_display = ('number', 'standard_name', 'cluster', 'group_name', 'parent', 'level', 'create_date')
    list_filter = ('cluster', 'group_name', 'type', 'parent', 'create_date')
    search_fields = ('standard_name', 'standard_name_latin', 'old_standard_code', 'cluster', 'group_name')
    ordering = ('number',)
    raw_id_fields = ('parent',)
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('number', 'standard_name', 'standard_name_latin', 'parent')
        }),
        ('طبقه‌بندی', {
            'fields': ('cluster', 'group_name', 'type')
        }),
        ('کدها', {
            'fields': ('old_standard_code', 'version', 'competency_code', 'isco_job_code', 'isco_group_code')
        }),
        ('سطح تحصیلات', {
            'fields': ('entry_education_level',)
        }),
        ('ساعات', {
            'fields': ('theoretical_hours', 'practical_hours', 'internship_hours', 'project_hours', 'total_hours')
        }),
        ('سایر اطلاعات', {
            'fields': ('work_and_knowledge', 'compilation_date')
        }),
    )
    
    def level(self, obj):
        return obj.level
    level.short_description = 'سطح'


admin.site.register(models.Comment)
admin.site.register(models.WishList)
