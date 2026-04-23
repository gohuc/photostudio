from django.contrib import admin
from .models import BookingType, ExtraService, Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'date', 'time', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'date', 'booking_type')
    search_fields = ('client_name', 'client_email', 'client_phone')
    readonly_fields = ('created_at', 'total_price')

@admin.register(BookingType)
class BookingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'is_active')
    list_editable = ('price', 'is_active')
    search_fields = ('name',)

@admin.register(ExtraService)
class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'order', 'is_active')
    list_editable = ('price', 'order', 'is_active')
    list_filter = ('category', 'is_active')