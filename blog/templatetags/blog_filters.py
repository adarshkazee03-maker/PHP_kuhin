"""
Blog template filters — clean, reusable tag utilities.
"""
from django import template

register = template.Library()


@register.filter(name='split_csv')
def split_csv(value, delimiter=','):
    """
    Split a comma-separated string into a list of stripped, non-empty strings.
    
    Usage in template:
        {% for tag in blog.tags|split_csv %}
            <span>{{ tag }}</span>
        {% endfor %}
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]


@register.filter(name='truncate_chars')
def truncate_chars(value, max_len=100):
    """Truncate to max_len characters, adding ellipsis if needed."""
    value = str(value)
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip() + '…'
