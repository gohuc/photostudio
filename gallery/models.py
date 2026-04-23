from django.db import models
from django.urls import reverse

class Album(models.Model):
    """Альбом для группировки фото"""
    name = models.CharField(max_length=100, verbose_name="Название альбома")
    slug = models.SlugField(unique=True, verbose_name="Ссылка (латиницей)")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover_image = models.ImageField(upload_to='albums/covers/', blank=True, null=True, verbose_name="Обложка")
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('gallery_album', args=[self.slug])

class GalleryImage(models.Model):
    """Фото в галерее"""
    title = models.CharField(max_length=200, verbose_name="Название")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='images', verbose_name="Альбом")
    image = models.ImageField(upload_to='gallery/', verbose_name="Фото")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(verbose_name='когда сделанны фотки')
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    
    def __str__(self):
        return self.title