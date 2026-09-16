from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Gallery Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    event_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title
