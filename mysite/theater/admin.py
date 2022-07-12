from django.contrib import admin
from .models import Genre, Performance, Director, Actor, PerformanceInstance

admin.site.register(Genre)
admin.site.register(Performance)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(PerformanceInstance)
