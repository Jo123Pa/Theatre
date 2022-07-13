from django.shortcuts import render
from django.http import HttpResponse
from .models import Genre, Performance, Director, Actor, PerformanceInstance

def index(request):
    num_performance = Performance.objects.count()
    num_instances = PerformanceInstance.objects.all().count()

    num_instances_available = PerformanceInstance.objects.filter(status__exact='Yra laisvų vietų').count()

    num_director = Director.objects.count()

    context = {
        'num_performance' : num_performance,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_director' : num_director,
    }

    return render(request, 'theater/index.html', context=context)


