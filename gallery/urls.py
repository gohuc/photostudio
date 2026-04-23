from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_page, name='gallery'),
    path('album/<slug:slug>/', views.album_detail, name='gallery_album'),
]