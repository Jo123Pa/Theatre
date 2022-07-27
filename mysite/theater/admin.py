from django.contrib import admin
from .models import Genre, Performance, Director, Actor, PerformanceInstance

class PerformanceInstanceInline(admin.TabularInline):
    model = PerformanceInstance
    extra = 0

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'director', 'genre', 'display_actor')
    inlines = [PerformanceInstanceInline]
    search_fields = ('id', 'title')

class PerformanceInstanceAdmin(admin.ModelAdmin):
    list_display = ('performance_date', 'performance', 'status', 'ticket')
    list_filter = ('performance_date', 'performance')

    fieldsets = (
        ('General', {'fields': ('unique_id', 'performance')}),
        ('Availability', {'fields': ('performance_date', 'status', 'viewer','ticket')}),
    )

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_performance')

admin.site.register(Genre)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor)
admin.site.register(PerformanceInstance, PerformanceInstanceAdmin)
