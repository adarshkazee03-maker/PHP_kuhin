"""
KUHIN — Development Settings
Override base settings for local development.
Run with: python manage.py runserver --settings=kuhin_project.settings.dev
"""
from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# Use simple static storage (no manifest compression in dev)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Console email — prints to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Local file storage for media
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Disable HTTPS requirements in dev
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
