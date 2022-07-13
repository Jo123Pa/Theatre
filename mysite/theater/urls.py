from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('directors/', views.directors, name='directors'),
    path('directors/<int:director_id>', views.director, name='director'),

]