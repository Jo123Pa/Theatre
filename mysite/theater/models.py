from telnetlib import STATUS
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth import get_user_model
from datetime import date
from tinymce.models import HTMLField
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from PIL import Image

class Genre(models.Model):
    name = models.CharField(verbose_name =_('genre'), max_length=200, help_text=_('enter the genre of the performance'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

class Director(models.Model):
    first_name = models.CharField(verbose_name =_('first_name'), max_length=100)
    last_name = models.CharField(verbose_name =_('last_name'), max_length=100)
    description = models.TextField(verbose_name =_('description'), max_length=500, default='')

    class Meta:
        ordering = ['last_name', 'first_name']

    
    def get_absolute_url(self):
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def display_performance(self):
        return ', '.join(performance.title for performance in self.performance.all())

    display_performance.short_description = 'Performance'


    class Meta:
        verbose_name = _('director')
        verbose_name_plural = _('directors')


class Performance(models.Model):
    title = models.CharField(verbose_name =_('title'), max_length=200)
    author = models.CharField(verbose_name =_('author'), max_length=200)
    summary = models.TextField(verbose_name =_('summary'), max_length=500)
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, related_name='performance')
    actor = models.ManyToManyField('Actor', help_text=_('choose the actors of the play'))
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(verbose_name =_('cover'), upload_to='covers', null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cover = Image.open(self.cover.path)
        if cover.height > 500 or cover.width > 500:
            output_size = (500, 500)
            cover.thumbnail(output_size)
            cover.save(self.cover.path)

    def get_absolute_url(self):
        return reverse('performance-detail', args=[str(self.id)])

    def display_actor(self):
        return ', '.join(actor.first_name for actor in self.actor.all())

    display_actor.short_description = 'Actor'
    
    class Meta:
        verbose_name = _('performance')
        verbose_name_plural = _('performances')

class Actor(models.Model):
    first_name = models.CharField(verbose_name =_('first_name'), max_length=100)
    last_name = models.CharField(verbose_name =_('last_name'), max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    
    def get_absolute_url(self):
        return reverse('actor-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = _('actor')
        verbose_name_plural = _('actors')


class PerformanceInstance(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, help_text=(_('A unique ID for a performance')))
    performance = models.ForeignKey('Performance', on_delete=models.SET_NULL, null=True)
    performance_date = models.DateField(verbose_name =_('performance_date'), null=True, blank=True)
    viewer = models.ManyToManyField(get_user_model())
    ticket = models.IntegerField(verbose_name =_('ticket'), blank=False, null=False, default=0)


    @property
    def is_overdue(self):
        if self.performance_date and date.today() > self.performance_date:
            return True
        return False


    PERFORMANCE_STATUS = (
        ('available', _('available')),
        ('not available', _('not available')),
    )

    status = models.CharField(
        max_length=20,
        choices=PERFORMANCE_STATUS,
        default='available',
        help_text=_('status'),
    )

    class Meta:
        verbose_name = _('performanceinstance')
        verbose_name_plural = _('performanceinstances')
        ordering = ['performance_date']


    def __str__(self):
        return f'({self.performance.title}{self.viewer})'


class PerformanceInstanceQuerySet(models.QuerySet):
    def booked(self):
        return self.filter(models.Q(status__exact='not available'))