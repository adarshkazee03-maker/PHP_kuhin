"""
KUHIN Newsletter Views
======================
Handles news listing, news detail, and email subscription.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import NewsUpdate


def news_list(request):
    """List all active news updates, newest first."""
    news_updates = NewsUpdate.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_updates': news_updates})


def news_detail(request, slug):
    """Full detail view of a single news item with related sidebar."""
    news = get_object_or_404(NewsUpdate, slug=slug, is_active=True)
    related_news = (
        NewsUpdate.objects.filter(is_active=True)
        .exclude(slug=slug)
        .order_by('-created_at')[:5]
    )
    return render(request, 'news/news_detail.html', {
        'news': news,
        'related_news': related_news,
    })


def subscribe(request):
    """
    Handle newsletter subscription via POST.
    Returns a redirect so it works from any page (footer form).
    """
    if request.method == 'POST':
        from .models import Subscriber
        email = request.POST.get('email', '').strip()
        if email:
            _, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Subscribed! Welcome to the KUHIN newsletter.')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')

        # Redirect back to the referring page, or home
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)

    return redirect('/')
