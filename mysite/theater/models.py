from django.db import models
from django.urls import reverse
import uuid

class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite knygos žandrą')

    def __str__(self):
        return self.name

class Director(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    
    def get_absolute_url(self):
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Performance(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.CharField('Autorius', max_length=200)
    summary = models.TextField('Aprašymas', max_length=500)
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    actor = models.ManyToManyField('Actor', help_text='Pasirinkite spektaklio aktorius')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField('Cover', upload_to='covers', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('performance-detail', args=[str(self.id)])
    

class Actor(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    
    def get_absolute_url(self):
        return reverse('actor-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class PerformanceInstance(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, help_text=('A unique ID for a performance'))
    performance = models.ForeignKey('Performance', on_delete=models.SET_NULL, null=True)
    performance_date = models.DateField('Pasirodymas', null=True, blank=True)
    # client = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True))

    PERFORMANCE_STATUS = (
        ('Yra laisvų vietų', 'Yra laisvų vietų'),
        ('Nėra laisvų vietų', 'Nėra laisvų vietų'),

    )

    status = models.CharField(
        max_length=20,
        choices=PERFORMANCE_STATUS,
        blank=True,
        default='Yra laisvų vietų',
        help_text='Statusas',
    )

    class Meta:
        ordering = ['performance_date']


    def __str__(self):
        return f'{self.id} ({self.performance.title})'