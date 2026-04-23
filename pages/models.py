from django.db import models
        

class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero/', verbose_name="Фото для главной")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Hero image {self.id}"
    
    class Meta:
        verbose_name = "Фото на главной"
        verbose_name_plural = "Фото на главной"
