from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from homepage_features.models import Announcement, Testimonial, Achievement, MemberSpotlight, ActivityFeed
from blog.models import BlogPost
from newsletter.models import NewsUpdate
from events.models import Event
from members.models import Member
from resources.models import Resource


def enhanced_home(request):
    """
    Enhanced homepage with all interactive features
    """
    
    # Hero Section - Active Announcements
    announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now()
    )
    
    # Filter by end_date if set
    active_announcements = []
    for announcement in announcements:
        if announcement.is_currently_active():
            active_announcements.append(announcement)
    
    # Member Spotlight
    current_spotlights = MemberSpotlight.objects.filter(
        is_active=True,
        start_date__lte=timezone.now().date()
    ).select_related('member')
    
    active_spotlights = []
    for spotlight in current_spotlights:
        if spotlight.is_currently_active():
            active_spotlights.append(spotlight)
    
    # If no active spotlight, pick a random active member
    featured_member = active_spotlights[0] if active_spotlights else None
    if not featured_member:
        random_member = Member.objects.filter(is_active=True).order_by('?').first()
        if random_member:
            featured_member = {
                'member': random_member,
                'spotlight_title': 'Featured Member',
                'spotlight_text': random_member.bio or 'Active member of KUHIN',
                'key_achievement': random_member.position
            }
    
    # Latest Content
    latest_blogs = BlogPost.objects.filter(
        status='published'
    ).select_related('category').order_by('-created_at')[:3]
    
    latest_news = NewsUpdate.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    # Upcoming Events with countdown
    upcoming_events = Event.objects.filter(
        status='upcoming',
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')[:3]
    
    # Next immediate event for countdown
    next_event = upcoming_events.first() if upcoming_events else None
    
    # Achievements & Milestones
    featured_achievements = Achievement.objects.filter(
        is_featured=True
    ).order_by('display_order')[:4]
    
    # Testimonials
    testimonials = Testimonial.objects.filter(
        is_featured=True
    ).order_by('display_order')[:6]
    
    # Latest Activity Feed
    activity_feed = ActivityFeed.objects.all()[:10]
    
    # Stats for counter animation
    stats = {
        'total_members': Member.objects.filter(is_active=True).count(),
        'total_events': Event.objects.count(),
        'total_blogs': BlogPost.objects.filter(status='published').count(),
        'upcoming_events': Event.objects.filter(status='upcoming').count(),
        'total_resources': Resource.objects.count(),
        'total_news': NewsUpdate.objects.filter(is_active=True).count(),
    }
    
    # Trending Content - Get latest published blogs
    trending_blogs = BlogPost.objects.filter(
        status='published'
    ).select_related('category').order_by('-created_at')[:3]
    
    context = {
        # Hero section
        'announcements': active_announcements,
        
        # Member spotlight
        'featured_member': featured_member,
        
        # Latest content
        'latest_blogs': latest_blogs,
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
        'next_event': next_event,
        
        # Achievements
        'achievements': featured_achievements,
        
        # Testimonials
        'testimonials': testimonials,
        
        # Activity feed
        'activity_feed': activity_feed,
        
        # Stats
        'stats': stats,
        
        # Trending
        'trending_blogs': trending_blogs,
    }
    
    return render(request, 'home/enhanced_index.html', context)
