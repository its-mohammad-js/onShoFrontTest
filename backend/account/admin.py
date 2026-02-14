from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['phone_number']
    list_display = ['first_name', 'last_name', 'phone_number', 'role', 'last_login']
    list_filter = ['role', 'is_staff', 'is_active', 'is_verified']


@admin.register(models.Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'subdomain', 'display_order', 'is_active', 'is_verified', 'create_date']
    list_filter = ['is_active', 'is_verified', 'display_order', 'create_date']
    search_fields = ['name', 'subdomain', 'user__phone_number', 'user__email']
    actions = ['activate_selected', 'deactivate_selected', 'verify_selected', 'unverify_selected']
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('user', 'name', 'slug', 'description')
        }),
        ('اطلاعات وب', {
            'fields': ('website_url', 'subdomain', 'logo')
        }),
        ('مدارک', {
            'fields': ('national_card', 'license')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'is_verified', 'display_order')
        }),
        ('تاریخ‌ها', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['create_date', 'update_date']

    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected.short_description = 'Activate selected organizers'

    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_selected.short_description = 'Deactivate selected organizers'

    def verify_selected(self, request, queryset):
        # Get organizers that are not yet verified
        to_verify = queryset.filter(is_verified=False)
        count = to_verify.count()
        
        # Update is_verified to True (this will trigger SMS via save method)
        for organizer in to_verify:
            organizer.is_verified = True
            organizer.save()  # This will trigger the SMS sending in the save method
        
        if count > 0:
            self.message_user(request, f'{count} organizer(s) verified and SMS sent.')
        else:
            self.message_user(request, 'No organizers were verified (they were already verified).')
    verify_selected.short_description = 'Verify selected organizers'

    def unverify_selected(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_selected.short_description = 'Unverify selected organizers'


class RolePermissionInline(admin.TabularInline):
    model = models.RolePermission
    extra = 1  # تعداد فیلدهای خالی برای اضافه کردن پرمیژن جدید


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'create_date')
    search_fields = ('title', 'slug')
    inlines = [RolePermissionInline]


@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'create_date')
    search_fields = ('title', 'slug')


@admin.register(models.RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')


class OrganizerTeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'is_active', 'is_verified', 'create_date', 'update_date')
    search_fields = ('user__username', 'organization__name')
    list_filter = ('is_active', 'is_verified', 'create_date', 'update_date')
    ordering = ('-create_date',)
    actions = ['activate_selected', 'deactivate_selected', 'verify_selected', 'unverify_selected']

    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected.short_description = 'Activate selected organizer teachers'

    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_selected.short_description = 'Deactivate selected organizer teachers'

    def verify_selected(self, request, queryset):
        queryset.update(is_verified=True)
    verify_selected.short_description = 'Verify selected organizer teachers'

    def unverify_selected(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_selected.short_description = 'Unverify selected organizer teachers'


admin.site.register(models.OrganizerTeacher, OrganizerTeacherAdmin)


@admin.register(models.ManualUser)
class ManualUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastname', 'nationalcode', 'tel', 'career', 'create_date']
    search_fields = ['name', 'lastname', 'nationalcode', 'tel']
    list_filter = ['create_date', 'career']
    readonly_fields = ['create_date', 'update_date']
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('name', 'lastname', 'nationalcode', 'tel', 'birthdate')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('address', 'career')
        }),
        ('تاریخ‌ها', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )