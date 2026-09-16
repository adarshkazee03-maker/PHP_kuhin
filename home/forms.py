from django import forms
from django.core.exceptions import ValidationError
import re

class ContactForm(forms.Form):
    """Contact form for sending messages to KUHIN Club"""
    
    name = forms.CharField(
        min_length=2,
        max_length=100,
        required=True,
        error_messages={
            'required': 'Name is required. Please enter your full name.',
            'min_length': 'Name must be at least 2 characters long.',
            'max_length': 'Name must not exceed 100 characters.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name',
            'aria-label': 'Full Name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email address (e.g., user@example.com).',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'aria-label': 'Email Address'
        })
    )
    
    subject = forms.CharField(
        min_length=3,
        max_length=200,
        required=True,
        error_messages={
            'required': 'Subject is required.',
            'min_length': 'Subject must be at least 3 characters long.',
            'max_length': 'Subject must not exceed 200 characters.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message Subject',
            'aria-label': 'Subject'
        })
    )
    
    message = forms.CharField(
        min_length=10,
        max_length=5000,
        required=True,
        error_messages={
            'required': 'Message is required.',
            'min_length': 'Message must be at least 10 characters long.',
            'max_length': 'Message must not exceed 5000 characters.',
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message...',
            'rows': 6,
            'aria-label': 'Message'
        })
    )
    
    def clean_name(self):
        """Validate name field with enhanced checks"""
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('Name is required. Please enter your full name.')
        
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        if len(name) > 100:
            raise ValidationError('Name must not exceed 100 characters.')
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError('Name can only contain letters, spaces, hyphens, and apostrophes.')
        
        # Check for minimum word count (at least 2 parts for full name)
        name_parts = name.split()
        if len(name_parts) < 2:
            raise ValidationError('Please enter your full name (first and last name).')
        
        return name
    
    def clean_email(self):
        """Validate email field with enhanced checks"""
        email = self.cleaned_data.get('email', '').strip()
        
        if not email:
            raise ValidationError('Email is required.')
        
        if len(email) > 254:
            raise ValidationError('Email address is too long.')
        
        # Additional email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError('❌ Email address is incorrect. Please enter a valid email (e.g., john@example.com).')
        
        # Check for disposable email domains (common spam)
        disposable_domains = [
            'tempmail', 'guerrillamail', '10minutemail', 'mailinator',
            'temp-mail', 'throwaway', 'fakeinbox', 'yopmail'
        ]
        domain = email.split('@')[1].lower()
        for disposable in disposable_domains:
            if disposable in domain:
                raise ValidationError('❌ Email address is incorrect. Please use a valid, permanent email address.')
        
        # Check for consecutive dots or invalid patterns
        if '..' in email:
            raise ValidationError('❌ Email address is incorrect. Email contains invalid characters.')
        
        return email.lower()
    
    def clean_subject(self):
        """Validate subject field with enhanced checks"""
        subject = self.cleaned_data.get('subject', '').strip()
        
        if not subject:
            raise ValidationError('Subject is required.')
        
        if len(subject) < 3:
            raise ValidationError('Subject must be at least 3 characters long.')
        
        if len(subject) > 200:
            raise ValidationError('Subject must not exceed 200 characters.')
        
        # Check for minimum word count
        words = subject.split()
        if len(words) < 2:
            raise ValidationError('Subject should be at least 2 words.')
        
        return subject
    
    def clean_message(self):
        """Validate message field with enhanced spam detection"""
        message = self.cleaned_data.get('message', '').strip()
        
        if not message:
            raise ValidationError('Message is required.')
        
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        if len(message) > 5000:
            raise ValidationError('Message must not exceed 5000 characters.')
        
        message_lower = message.lower()
        
        # Enhanced spam patterns with more comprehensive checks
        spam_patterns = [
            (r'\b(viagra|cialis|phentermine|tramadol)\b', 'pharmaceutical spam'),
            (r'\b(casino|poker|slots|blackjack|lottery|prize|jackpot)\b', 'gambling spam'),
            (r'\b(click here|buy now|limited offer|act now|limited time)\b', 'aggressive marketing'),
            (r'\b(free money|make money|earn money|work from home)\b', 'financial scam'),
            (r'http[s]?://\S+', 'suspicious links'),
            (r'(<a href|<script|javascript:)', 'HTML/script injection'),
            (r'(.)\1{2,}', 'repeated characters'),  # Multiple consecutive identical chars (e.g., "hellooooo")
        ]
        
        for pattern, description in spam_patterns:
            try:
                if re.search(pattern, message_lower):
                    raise ValidationError(f'Message contains prohibited content ({description}). Please try again.')
            except Exception as e:
                # If regex fails, continue without this check
                continue
        
        # Check for excessive punctuation
        punctuation_count = len(re.findall(r'[!?]{2,}', message))
        if punctuation_count > 3:
            raise ValidationError('Message contains excessive punctuation. Please use standard punctuation.')
        
        # Check for minimum word count (meaningful message)
        words = message.split()
        if len(words) < 5:
            raise ValidationError('Message should contain at least 5 words.')
        
        # Check for repetitive words
        word_freq = {}
        for word in words:
            if len(word) > 2:  # Only count words longer than 2 chars
                word_freq[word.lower()] = word_freq.get(word.lower(), 0) + 1
        
        for word, count in word_freq.items():
            if count > 5:  # If same word appears more than 5 times
                raise ValidationError('Message contains too many repeated words.')
        
        return message
