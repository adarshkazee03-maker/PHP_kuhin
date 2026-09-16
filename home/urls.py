from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('team/', views.team, name='team'),
    path('team/<int:pk>/', views.member_detail, name='member_detail'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('resources/', views.resources, name='resources'),
    path('resources/<slug:slug>/', views.resource_detail, name='resource_detail'),
    path('contact/', views.contact, name='contact'),
]
