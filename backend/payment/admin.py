from django.contrib import admin

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'create_date', 'update_date')
    list_filter = ('status', 'create_date')
    search_fields = ('user__username', 'user__email')
    ordering = ('-create_date',)


@admin.register(models.CourseOrder)
class CourseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'course', 'quantity', 'price', 'discount', 'final_price', 'create_date')
    list_filter = ('order', 'course')
    search_fields = ('order__id', 'course__title')
    ordering = ('-create_date',)


@admin.register(models.PurchaseCode)
class PurchaseCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'course', 'organization', 'purchased_by', 'total_credits', 'remaining_credits', 'is_active', 'create_date')
    list_filter = ('is_active', 'organization', 'create_date')
    search_fields = ('code', 'course__title', 'organization__name', 'purchased_by__phone_number')
    ordering = ('-create_date',)
    readonly_fields = ('code', 'create_date', 'update_date')


@admin.register(models.CodeRedemption)
class CodeRedemptionAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'course', 'redeemed_at')
    list_filter = ('redeemed_at', 'course')
    search_fields = ('code__code', 'user__phone_number', 'course__title')
    ordering = ('-redeemed_at',)
    readonly_fields = ('redeemed_at',)


admin.site.register(models.Status)
admin.site.register(models.Situation)
admin.site.register(models.Transaction)
admin.site.register(models.PaymentGateway)
