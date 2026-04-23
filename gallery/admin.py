from django.contrib import admin
from .models import Album, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('title', 'image', 'order', 'is_active')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryImageInline]
    search_fields = ('name', 'description')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('album', 'is_active')
    search_fields = ('title', 'description')