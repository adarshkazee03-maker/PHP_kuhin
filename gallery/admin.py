from django.contrib import admin
from .models import GalleryCategory, GalleryImage

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    readonly_fields = ['uploaded_at']
