from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update_profile, name = 'profile-update'),
]