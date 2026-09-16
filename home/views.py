"""
KUHIN Home App — Views
======================
All main site page views. Keeps logic minimal and readable.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from events.models import Event
from members.models import Member
from blog.models import BlogPost
from .forms import ContactForm
from .email_utils import (
    get_client_ip, check_rate_limit,
    increment_rate_limit, send_contact_email, send_confirmation_email,
)


# ── HOME ─────────────────────────────────────────────────────────
def home(request):
    upcoming_events = (
        Event.objects.filter(date__gte=timezone.now().date())
        .order_by('date')[:6]
    )
    latest_blogs = (
        BlogPost.objects.filter(status='published')
        .select_related('category', 'author')
        .order_by('-published_date')[:3]
    )
    testimonial_members = (
        Member.objects.filter(is_active=True)
        .order_by('display_order', 'name')[:3]
    )
    return render(request, 'home.html', {
        'upcoming_events': upcoming_events,
        'latest_blogs': latest_blogs,
        'testimonial_members': testimonial_members,
        'members_count': Member.objects.filter(is_active=True).count(),
        'events_count': Event.objects.count(),
    })


# ── ABOUT / PROGRAMS ─────────────────────────────────────────────
def about(request):
    return render(request, 'about.html')


def programs(request):
    return render(request, 'programs.html')


# ── TEAM ─────────────────────────────────────────────────────────
def team(request):
    return render(request, 'team.html', {
        'executive_committee': Member.objects.filter(
            team='Executive Committee'
        ).order_by('display_order', 'name'),
        'advisory_board': Member.objects.filter(
            team='Advisory Board'
        ).order_by('display_order', 'name'),
    })


def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'member_detail.html', {'member': member})


# ── EVENTS ───────────────────────────────────────────────────────
def events(request):
    return render(request, 'events.html', {
        'upcoming_events': Event.objects.filter(status='upcoming').order_by('date'),
        'past_events': Event.objects.filter(status='completed').order_by('-date'),
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = (
        Event.objects.filter(status='upcoming')
        .exclude(slug=slug)
        .order_by('date')[:3]
    )
    return render(request, 'event_detail.html', {
        'event': event,
        'related_events': related_events,
    })


# ── GALLERY ──────────────────────────────────────────────────────
def gallery(request):
    from gallery.models import GalleryImage, GalleryCategory
    category_slug = request.GET.get('category', '')
    images = GalleryImage.objects.select_related('category').all()
    if category_slug:
        images = images.filter(category__slug=category_slug)
    categories = GalleryCategory.objects.all()
    return render(request, 'gallery.html', {
        'images': images,
        'categories': categories,
        'selected_category': category_slug,
    })


# ── RESOURCES ────────────────────────────────────────────────────
def resources(request):
    from resources.models import Resource, ResourceCategory
    category_slug = request.GET.get('category', '')
    qs = Resource.objects.select_related('category').all()
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    return render(request, 'resources.html', {
        'resources': qs,
        'categories': ResourceCategory.objects.all(),
        'selected_category': category_slug,
    })


def resource_detail(request, slug):
    from resources.models import Resource
    resource = get_object_or_404(Resource, slug=slug)
    related = (
        Resource.objects.filter(category=resource.category)
        .exclude(slug=slug)
        .select_related('category')
        .order_by('-uploaded_at')[:4]
    )
    return render(request, 'resource_detail.html', {
        'resource': resource,
        'related_resources': related,
    })


# ── CONTACT ──────────────────────────────────────────────────────
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            client_ip = get_client_ip(request)
            is_allowed, _, _ = check_rate_limit(client_ip)
            if not is_allowed:
                messages.error(
                    request,
                    'Too many messages. Please wait an hour before trying again.',
                )
                return render(request, 'contact.html', {'form': form})

            result = send_contact_email(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                request=request,
            )
            if result.get('success'):
                increment_rate_limit(client_ip)
                send_confirmation_email(
                    form.cleaned_data['email'],
                    form.cleaned_data['name'],
                )
                messages.success(request, "Message sent! We'll get back to you within 1–2 business days.")
                return redirect('home:contact')
            else:
                messages.error(request, result.get('error', 'Could not send message. Please try again.'))
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ── ERROR HANDLERS ───────────────────────────────────────────────
def handler404(request, exception=None):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
