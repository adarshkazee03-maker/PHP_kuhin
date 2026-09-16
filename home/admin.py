from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at_formatted', 'status_badge', 'replied_badge')
    list_filter = ('is_read', 'replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'name', 'email', 'subject', 'message', 'full_details')
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'replied'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_replied', 'mark_as_not_replied']
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y - %I:%M %p")
    created_at_formatted.short_description = 'Date & Time'
    
    def status_badge(self, obj):
        if obj.is_read:
            color = '#28a745'
            status = 'Read'
        else:
            color = '#ffc107'
            status = 'Unread'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'
    
    def replied_badge(self, obj):
        if obj.replied:
            color = '#28a745'
            status = 'Replied'
        else:
            color = '#dc3545'
            status = 'Pending'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            status
        )
    replied_badge.short_description = 'Reply Status'
    
    def full_details(self, obj):
        return format_html(
            '<div style="white-space: pre-wrap; line-height: 1.6; font-family: monospace;">{}</div>',
            obj.message
        )
    full_details.short_description = 'Full Message'
    
    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    
    @admin.action(description='Mark selected messages as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    
    @admin.action(description='Mark selected as replied')
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} message(s) marked as replied.')
    
    @admin.action(description='Mark selected as not replied')
    def mark_as_not_replied(self, request, queryset):
        updated = queryset.update(replied=False)
        self.message_user(request, f'{updated} message(s) marked as not replied.')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
