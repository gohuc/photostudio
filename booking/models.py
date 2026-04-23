from django.db import models
from django.contrib.auth.models import User

class BookingType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') 
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    duration_minutes = models.CharField(max_length=20, verbose_name='Длительность')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тип бронирования'
        verbose_name_plural = 'Типы бронирования'

class ExtraService(models.Model):
    category = models.CharField(max_length=100, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название') 
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Дополнительные услуги'
        verbose_name_plural = 'Дополнительные услуги'



class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
    ]
    class Meta:
        unique_together = ['date', 'time']
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
    
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    booking_type = models.ForeignKey(BookingType, on_delete=models.PROTECT, null=True, blank=True)
    package_name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()          
    time = models.TimeField()          
    extra_services = models.ManyToManyField(ExtraService, blank=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)