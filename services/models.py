from django.db import models
from django.urls import reverse

class Package(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название пакета")
    slug = models.SlugField(unique=True, verbose_name="Ссылка")
    description = models.TextField(verbose_name="Описание")
    duration = models.CharField(max_length=50, verbose_name="Длительность")
    duration_minutes = models.CharField(max_length=50, verbose_name='Длительность в минутах')
    photos_count = models.CharField(max_length=50, verbose_name="Количество фото")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    includes = models.TextField(verbose_name="Что входит (маркированный список)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Пакеты'
        verbose_name_plural = 'Пакеты'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('package_detail', args=[self.slug])