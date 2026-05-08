from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('skills/', views.skills, name='skills'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact, name='contact'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),
]
