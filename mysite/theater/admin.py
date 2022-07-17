from django.contrib import admin
from .models import Genre, Performance, Director, Actor, PerformanceInstance

class PerformanceInstanceInline(admin.TabularInline):
    model = PerformanceInstance
    # readonly_fields = ('id',)
    # can_delete = False
    extra = 0

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'director', 'genre', 'display_actor')
    inlines = [PerformanceInstanceInline]
    search_fields = ('id', 'title')

class PerformanceInstanceAdmin(admin.ModelAdmin):
    list_display = ('performance_date', 'performance', 'status', 'viewer')
    # list_editable = ('performance_date', 'status')
    list_filter = ('performance_date', 'performance')
    # search_fields = ('id', 'performance__title')

    fieldsets = (
        ('General', {'fields': ('unique_id', 'performance')}),
        ('Availability', {'fields': ('performance_date', 'status', 'viewer')}),
    )

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_performance')

admin.site.register(Genre)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor)
admin.site.register(PerformanceInstance, PerformanceInstanceAdmin)
