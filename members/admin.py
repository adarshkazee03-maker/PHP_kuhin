from django.contrib import admin
from django.utils.html import format_html
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'team', 'batch', 'is_active_badge', 'display_order')
    list_filter = ('team', 'position', 'batch', 'is_active')
    search_fields = ('name', 'email', 'role_in_project')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'email', 'phone', 'batch')
        }),
        ('Position & Team', {
            'fields': ('position', 'team', 'role_in_project', 'specialization')
        }),
        ('Biography & Achievements', {
            'fields': ('bio', 'achievements'),
            'classes': ('collapse',)
        }),
        ('Social Links', {
            'fields': ('linkedin', 'github', 'twitter', 'website'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order', 'join_date', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            color = '#28a745'
            status = 'Active'
        else:
            color = '#dc3545'
            status = 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status
        )
    is_active_badge.short_description = 'Status'
    
    ordering = ('team', 'display_order', 'name')
