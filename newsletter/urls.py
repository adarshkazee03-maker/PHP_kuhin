from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
