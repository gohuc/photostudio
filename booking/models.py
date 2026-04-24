from django.db import models
from django.contrib.auth.models import User
from services.models import Package

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
        ('completed', 'Завершена')
    ]
    
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    client_email = models.EmailField(verbose_name='Почта клиента')
    client_phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    booking_type = models.ForeignKey(BookingType, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тип бронирования')
    selected_package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Выбранный пакет')
    date = models.DateField(verbose_name='Дата')          
    time = models.TimeField(verbose_name='Время')          
    extra_services = models.ManyToManyField(ExtraService, blank=True, verbose_name='Доп услуги') 
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Сумма заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')

    class Meta:
        unique_together = ['date', 'time']
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        if self.selected_package:
            return f"{self.client_name} - {self.selected_package.name} - {self.date}"
        return f"{self.client_name} - {self.booking_type} - {self.date}"