from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from members.models import Member


class Announcement(models.Model):
    """Homepage announcement/hero banner"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    background_color = models.CharField(
        max_length=7,
        default='#667eea',
        help_text='Hex color code (e.g., #667eea)'
    )
    button_text = models.CharField(max_length=100, default='Learn More', blank=True)
    button_link = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def is_currently_active(self):
        """Check if announcement is currently active based on date range"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True


class Testimonial(models.Model):
    """Member testimonials for homepage"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    testimonial_text = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Achievement(models.Model):
    """Club achievements and milestones"""
    ACHIEVEMENT_TYPES = [
        ('award', 'Award'),
        ('milestone', 'Milestone'),
        ('record', 'Record'),
        ('certification', 'Certification'),
        ('event', 'Event'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    date_achieved = models.DateField()
    
    icon = models.CharField(
        max_length=50,
        default='fa-trophy',
        help_text='Font Awesome icon class (e.g., fa-trophy)'
    )
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    
    stat_value = models.CharField(max_length=100, blank=True, help_text='E.g., 500, 1000+')
    stat_label = models.CharField(max_length=100, blank=True, help_text='E.g., Members, Events')
    
    is_featured = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
        ordering = ['display_order', '-date_achieved']
    
    def __str__(self):
        return f"{self.title} ({self.achievement_type})"


class MemberSpotlight(models.Model):
    """Spotlight featured member on homepage"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    spotlight_title = models.CharField(max_length=200, default='Member Spotlight')
    spotlight_text = models.TextField(blank=True, help_text='Custom spotlight description')
    key_achievement = models.CharField(max_length=300, blank=True)
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Member Spotlight'
        verbose_name_plural = 'Member Spotlights'
        ordering = ['display_order', '-start_date']
    
    def __str__(self):
        return f"{self.member.name} - {self.spotlight_title}"
    
    def is_currently_active(self):
        """Check if spotlight is currently active based on date range"""
        today = timezone.now().date()
        if not self.is_active:
            return False
        if self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True


class ActivityFeed(models.Model):
    """Activity feed for homepage"""
    ACTIVITY_TYPES = [
        ('blog', 'Blog Post'),
        ('news', 'News Update'),
        ('event', 'Event'),
        ('member', 'Member Joined'),
        ('achievement', 'Achievement'),
        ('resource', 'Resource Added'),
    ]
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        default='fa-bell',
        help_text='Font Awesome icon class'
    )
    
    # Link to related object (optional)
    link_url = models.URLField(blank=True)
    
    # For auto-generation tracking
    auto_generated = models.BooleanField(default=True)
    related_content_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Feed'
        verbose_name_plural = 'Activity Feeds'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title}"
    
    @classmethod
    def create_blog_activity(cls, blog_post):
        """Auto-create activity for new blog post"""
        return cls.objects.create(
            activity_type='blog',
            title=f'New Blog: {blog_post.title}',
            description=blog_post.content[:150],
            icon='fa-newspaper',
            link_url=blog_post.get_absolute_url() if hasattr(blog_post, 'get_absolute_url') else '',
            auto_generated=True,
            related_content_type='blog',
            related_object_id=blog_post.id
        )
    
    @classmethod
    def create_news_activity(cls, news_update):
        """Auto-create activity for new news update"""
        return cls.objects.create(
            activity_type='news',
            title=f'News: {news_update.title}',
            description=news_update.description[:150],
            icon='fa-bullhorn',
            link_url=news_update.get_absolute_url() if hasattr(news_update, 'get_absolute_url') else '',
            auto_generated=True,
            related_content_type='news',
            related_object_id=news_update.id
        )
    
    @classmethod
    def create_event_activity(cls, event):
        """Auto-create activity for new event"""
        return cls.objects.create(
            activity_type='event',
            title=f'Event: {event.title}',
            description=event.description[:150] if hasattr(event, 'description') else '',
            icon='fa-calendar',
            link_url=event.get_absolute_url() if hasattr(event, 'get_absolute_url') else '',
            auto_generated=True,
            related_content_type='event',
            related_object_id=event.id
        )
