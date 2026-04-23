from django.shortcuts import render, get_object_or_404
from .models import Album, GalleryImage

def gallery_page(request):
    albums = Album.objects.filter(is_active=True)
    return render(request, 'gallery/gallery.html', {'albums': albums})

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, is_active=True)
    images = album.images.filter(is_active=True)
    return render(request, 'gallery/album.html', {'album': album, 'images': images})