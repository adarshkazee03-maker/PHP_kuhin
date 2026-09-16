from django.db import models
from ckeditor.fields import RichTextField

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Workshop', 'Workshop'),
        ('Seminar', 'Seminar'),
        ('Conference', 'Conference'),
        ('Webinar', 'Webinar'),
        ('Competition', 'Competition'),
        ('Hackathon', 'Hackathon'),
        ('Meeting', 'Meeting'),
        ('Social', 'Social Event'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    description = RichTextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    venue_link = models.URLField(blank=True, help_text="Google Maps or virtual meeting link")
    image = models.ImageField(upload_to='events/', blank=True)
    banner = models.ImageField(upload_to='events/banners/', blank=True)
    registration_link = models.URLField(blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    speakers = models.TextField(blank=True, help_text="Speaker names, comma-separated")
    prerequisites = RichTextField(blank=True)
    outcome = RichTextField(blank=True, help_text="What participants will learn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    batch = models.CharField(max_length=10)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['event', 'email']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
