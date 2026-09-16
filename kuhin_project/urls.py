"""
KUHIN Project — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# CKEditor file upload URL
try:
    from django.urls import re_path
    import ckeditor_uploader.urls as ckeditor_urls
    ckeditor_available = True
except ImportError:
    ckeditor_available = False

urlpatterns = [
    path('admin/', admin.site.urls),
    # CKEditor file uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Home app: /, /about/, /programs/, /team/, /events/, /gallery/, /resources/, /contact/
    path('', include('home.urls')),
    # Blog: /blogs/, /blogs/<slug>/
    path('blogs/', include('blog.urls')),
    # Newsletter: /news/, /news/<slug>/, /subscribe/
    path('', include('newsletter.urls')),
]

# Custom error handlers
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'

# Serve uploaded media files in development (DEBUG=True)
# In production, media is served by Nginx or Cloudinary
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Note: static files in dev are served by Django's built-in runserver
    # Do NOT add static() here — it conflicts with WhiteNoise
