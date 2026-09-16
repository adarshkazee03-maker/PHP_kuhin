"""Email utilities and rate limiting for the contact form"""

from django.core.mail import EmailMessage
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_KEY_TEMPLATE = 'contact_form_limit_{ip}'
RATE_LIMIT_MAX_MESSAGES = 5
RATE_LIMIT_WINDOW_SECONDS = 3600  # 1 hour


def get_client_ip(request):
    """
    Extract client IP address from request
    Handles proxy headers for production environments
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If there are multiple IPs, get the first one (client IP)
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_rate_limit(ip_address):
    """
    Check if IP address has exceeded rate limit
    Returns: (is_allowed: bool, remaining_messages: int, reset_time: str)
    """
    cache_key = RATE_LIMIT_KEY_TEMPLATE.format(ip=ip_address)
    message_count = cache.get(cache_key, 0)
    
    is_allowed = message_count < RATE_LIMIT_MAX_MESSAGES
    remaining = max(0, RATE_LIMIT_MAX_MESSAGES - message_count)
    
    return is_allowed, remaining, message_count


def increment_rate_limit(ip_address):
    """
    Increment message count for IP address
    """
    cache_key = RATE_LIMIT_KEY_TEMPLATE.format(ip=ip_address)
    message_count = cache.get(cache_key, 0)
    cache.set(cache_key, message_count + 1, RATE_LIMIT_WINDOW_SECONDS)


def send_contact_email(name, email, subject, message, request=None):
    """
    Send contact form email to KUHIN
    
    Args:
        name (str): Sender's name
        email (str): Sender's email address
        subject (str): Email subject
        message (str): Email message body
        request (HttpRequest): Optional request object for IP logging
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'error': str or None
        }
    """
    try:
        # Email configuration
        recipient_email = getattr(settings, 'CONTACT_EMAIL_RECIPIENT', 'kuhin@ku.edu.np')
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@kuhin.ku.edu.np')
        
        # Format the email body
        email_body = f"""
Hello KUHIN Team,

You have received a new message from the contact form:

{'='*60}
NAME: {name}
EMAIL: {email}
SUBJECT: {subject}
{'='*60}

MESSAGE:
{message}

{'='*60}

This is an automated email. Please reply to the sender's email address above.

Best regards,
KUHIN Website
        """.strip()
        
        # Create email message with reply-to
        email_message = EmailMessage(
            subject=f"[KUHIN Contact Form] {subject}",
            body=email_body,
            from_email=sender_email,
            to=[recipient_email],
            reply_to=[email],
        )
        
        # Send the email
        email_message.send(fail_silently=False)
        
        # Log successful email send
        logger.info(
            f"Contact form email sent successfully from {email} (IP: {request.META.get('REMOTE_ADDR') if request else 'Unknown'})"
        )
        
        return {
            'success': True,
            'message': 'Your message has been sent successfully! We will get back to you soon.',
            'error': None
        }
    
    except Exception as e:
        # Log the error
        logger.error(f"Failed to send contact form email: {str(e)}", exc_info=True)
        
        return {
            'success': False,
            'message': None,
            'error': 'Failed to send your message. Please try again later or contact us directly at kuhin@ku.edu.np'
        }


def send_confirmation_email(email, name):
    """
    Send confirmation email to the user who submitted the form
    
    Args:
        email (str): User's email address
        name (str): User's name
    
    Returns:
        dict: Success/failure information
    """
    try:
        sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@kuhin.ku.edu.np')
        
        email_body = f"""
Hi {name},

Thank you for reaching out to KUHIN - Kathmandu University Health Informatics Club!

We have received your message and will review it shortly. 
Our team typically responds within 24-48 hours.

If your inquiry is urgent, please feel free to contact us directly at:
📧 kuhin@ku.edu.np

Best regards,
KUHIN Team
Kathmandu University
        """.strip()
        
        email_message = EmailMessage(
            subject="We've received your message - KUHIN",
            body=email_body,
            from_email=sender_email,
            to=[email],
        )
        
        email_message.send(fail_silently=False)
        
        logger.info(f"Confirmation email sent to {email}")
        
        return {
            'success': True,
            'error': None
        }
    
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {email}: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }
