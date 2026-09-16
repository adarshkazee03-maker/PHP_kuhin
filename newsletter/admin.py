from django.contrib import admin
from .models import Subscriber, NewsUpdate

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']

@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

