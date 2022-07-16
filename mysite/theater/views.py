from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Genre, Performance, Director, Actor, PerformanceInstance
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator

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

def directors(request):

    directors = Director.objects.all()
    context = {
        'directors' : directors
    }
    return render(request, 'theater/directors.html', context=context)


def director(request, director_id):
    single_director = get_object_or_404(Director, pk=director_id)
    return render(request, 'theater/director.html', {'director': single_director})

def actors(request):
    paginator = Paginator(Actor.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_actors = paginator.get_page(page_number)
    context = {
        'actors' : paged_actors
    }
    return render(request, 'theater/actors.html', context=context)

def actor(request, actor_id):
    single_actor = get_object_or_404(Actor, pk=actor_id)
    return render(request, 'theater/actor.html', {'actor': single_actor})

class PerformanceListView(generic.ListView):
    model = Performance
    # queryset = Performance.objects.filter(status__exact='Yra laisvų vietų')[:3] 
    paginate_by = 1
    template_name = 'theater/performance_list.html'

class PerformanceDetailView(generic.DetailView):
    model = Performance
    context = 'performance'
    template_name = 'theater/performance_detail.html'


def search(request):
    query = request.GET.get('query')
    search_results = Performance.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
    context = {
        "query": query,
        "performances": search_results,
    }
    return render(request, 'theater/search.html', context=context)

