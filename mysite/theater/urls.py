from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('directors/', views.directors, name='directors'),
    path('directors/<int:director_id>', views.director, name='director'),
    path('actors/', views.actors, name='actors'),
    path('actors/<int:actor_id>', views.actor, name='actor'),
    path('performances/', views.PerformanceListView.as_view(), name='performances'),
    path('performances/<int:pk>', views.PerformanceDetailView.as_view(), name='performance-detail'),
    
]