"""Resources admin — clean forms with proper validation."""
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import ResourceCategory, Resource


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'resource_type', 'uploaded_by', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'resource_type', 'is_featured']
    search_fields = ['title', 'tags', 'uploaded_by']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']
    readonly_fields = ['uploaded_at', 'updated_at']
    date_hierarchy = 'uploaded_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'resource_type', 'description'),
        }),
        ('Resource Content', {
            'fields': ('file', 'external_link'),
            'description': (
                'Provide at least one: a file upload OR an external link. '
                'For link-type resources, use "External link". '
                'For documents, upload a file.'
            ),
        }),
        ('Media & Meta', {
            'fields': ('thumbnail', 'uploaded_by', 'tags', 'is_featured'),
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Run model-level clean() before saving."""
        try:
            obj.clean()
        except ValidationError as e:
            # Surface the error to the admin user cleanly
            from django.contrib import messages
            messages.error(request, f'Validation error: {e.message}')
            return  # Don't save
        super().save_model(request, obj, form, change)
