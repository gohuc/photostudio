from django.shortcuts import render
from services.models import Package
from gallery.models import GalleryImage
from .models import HeroImage 

def home(request):
    packages = Package.objects.filter(is_active=True)[:3]
    recent_photos = GalleryImage.objects.filter(is_active=True)[:6]
    hero_image = HeroImage.objects.filter(is_active=True).first()

    context = {
        'packages': packages,
        'recent_photos': recent_photos,
        'hero_image': hero_image,
    }
    return render(request, 'pages/home.html', context)

def about(request):
    return render(request, 'pages/about.html')