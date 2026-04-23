from django.contrib import admin
from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'duration_minutes', 'is_active', 'order')
    list_editable = ('price', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')