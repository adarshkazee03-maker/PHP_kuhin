from django.db import models
from ckeditor.fields import RichTextField

class Member(models.Model):
    POSITION_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Technical Lead', 'Technical Lead'),
        ('Research Head', 'Research Head'),
        ('Media Head', 'Media Head'),
        ('Senior Member', 'Senior Member'),
        ('Junior Member', 'Junior Member'),
        ('Core Member', 'Core Member'),
        ('Advisory Board Member', 'Advisory Board Member'),
        ('Executive Committee Member', 'Executive Committee Member'),
    ]
    
    BATCH_CHOICES = [
    
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030'),
        ('2031', '2031'),
        ('2032', '2032'),
        ('2033', '2033'),
        ('2034', '2034'),
        ('2035', '2035'),
        ('2036', '2036'),
        ('2037', '2037'),
        ('2038', '2038'),
        ('2039', '2039'),
        ('2040', '2040'),     
    ]
    
    TEAM_CHOICES = [
        ('Executive Committee', 'Executive Committee'),
        ('Advisory Board', 'Advisory Board'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    team = models.CharField(max_length=50, choices=TEAM_CHOICES, default='Executive Committee')
    role_in_project = models.CharField(max_length=100)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES)
    bio = RichTextField(max_length=1000)
    photo = models.ImageField(upload_to='members/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    join_date = models.DateField(null=True, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    achievements = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['team', 'display_order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
    
    def __str__(self):
        return f"{self.name} - {self.position}"
