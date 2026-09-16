from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'start_time', 'status', 'is_featured']
    list_filter = ['event_type', 'status', 'date', 'is_featured']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    list_editable = ['status', 'is_featured']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'email', 'batch', 'registered_at', 'attended']
    list_filter = ['event', 'attended', 'registered_at']
    search_fields = ['name', 'email']
    list_editable = ['attended']
    readonly_fields = ['registered_at']
