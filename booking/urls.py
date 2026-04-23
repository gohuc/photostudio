from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_page, name='booking'),
    path('submit-booking/', views.submit_booking, name='submit_booking'),
    path('get-available-slots/', views.get_available_slots, name='get_available_slots'),
]