"""
Resources app models.
The 'file' field exists in migrations with blank=True — we keep it here
explicitly with blank=True, null=True so admin submissions never hit a
NOT NULL constraint regardless of DB state.
"""
from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-file')

    class Meta:
        verbose_name_plural = 'Resource Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Resource(models.Model):
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('link', 'External Link'),
        ('video', 'Video'),
        ('tool', 'Tool/Software'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # File upload (optional — resources can be link-only)
    file = models.FileField(
        upload_to='resources/files/',
        blank=True,
        null=True,
        help_text='Optional file upload (PDF, DOCX, etc.)',
    )
    external_link = models.URLField(
        blank=True,
        help_text='Optional external URL (used if no file is uploaded)',
    )
    thumbnail = models.ImageField(
        upload_to='resources/thumbnails/',
        blank=True,
        null=True,
    )

    uploaded_by = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text='Comma-separated tags, e.g. "python, health, fhir"',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def clean(self):
        """Require at least one of: file or external_link."""
        if not self.file and not self.external_link:
            raise ValidationError(
                'Please provide either a file upload or an external link URL.'
            )

    @property
    def access_url(self):
        """Return the primary access URL for this resource."""
        if self.file:
            return self.file.url
        return self.external_link or ''
