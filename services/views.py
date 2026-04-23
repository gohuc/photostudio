from django.shortcuts import render, get_object_or_404
from .models import Package

def packages_list(request):
    """Страница со списком всех пакетов"""
    packages = Package.objects.filter(is_active=True)
    return render(request, 'services/packages.html', {'packages': packages})

def package_detail(request, slug):
    """Страница отдельного пакета с кнопкой бронирования"""
    package = get_object_or_404(Package, slug=slug, is_active=True)
    return render(request, 'services/package_detail.html', {'package': package})