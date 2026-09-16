from django.contrib import admin
from .models import Announcement, Testimonial, Achievement, MemberSpotlight, ActivityFeed


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'display_order', 'start_date', 'end_date', 'is_currently_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'subtitle', 'description']
    ordering = ['display_order', '-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Call to Action', {
            'fields': ('button_text', 'button_link')
        }),
        ('Visual', {
            'fields': ('image', 'background_color')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order', 'start_date', 'end_date')
        }),
    )
    
    def is_currently_active(self, obj):
        return obj.is_currently_active()
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Currently Active'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'rating', 'is_featured', 'display_order', 'created_at']
    list_filter = ['is_featured', 'rating', 'created_at']
    search_fields = ['name', 'position', 'testimonial_text']
    ordering = ['display_order', '-created_at']
    
    fieldsets = (
        ('Person', {
            'fields': ('name', 'position', 'photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial_text', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'achievement_type', 'is_featured', 'display_order', 'date_achieved']
    list_filter = ['achievement_type', 'is_featured', 'date_achieved']
    search_fields = ['title', 'description']
    ordering = ['display_order', '-date_achieved']
    date_hierarchy = 'date_achieved'
    
    fieldsets = (
        ('Achievement', {
            'fields': ('title', 'description', 'achievement_type', 'date_achieved')
        }),
        ('Visual', {
            'fields': ('icon', 'image')
        }),
        ('Statistics', {
            'fields': ('stat_value', 'stat_label')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
    )


@admin.register(MemberSpotlight)
class MemberSpotlightAdmin(admin.ModelAdmin):
    list_display = ['spotlight_title', 'member', 'is_active', 'display_order', 'start_date', 'end_date', 'is_currently_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['spotlight_title', 'spotlight_text', 'member__name']
    ordering = ['display_order', '-start_date']
    raw_id_fields = ['member']
    
    fieldsets = (
        ('Spotlight', {
            'fields': ('member', 'spotlight_title', 'spotlight_text', 'key_achievement')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order', 'start_date', 'end_date')
        }),
    )
    
    def is_currently_active(self, obj):
        return obj.is_currently_active()
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Currently Active'


@admin.register(ActivityFeed)
class ActivityFeedAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'title', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return True
