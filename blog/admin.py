from django.contrib import admin
from .models import Category, BlogPost

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'published_date', 'views']
    list_filter = ['status', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views', 'created_at', 'updated_at']
