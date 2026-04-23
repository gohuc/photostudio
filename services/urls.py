from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages_list, name='packages'),
    path('<slug:slug>/', views.package_detail, name='package_detail'),
]