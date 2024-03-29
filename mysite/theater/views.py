from django import views
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from .models import Genre, Performance, Director, Actor, PerformanceInstance
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

def index(request):
    num_performance = Performance.objects.count()
    num_instances = PerformanceInstance.objects.all().count()
    num_instances_available = PerformanceInstance.objects.filter(status__exact='available').count()
    num_director = Director.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_performance' : num_performance,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_director' : num_director,
        'num_visits' : num_visits,
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
    paginator = Paginator(Actor.objects.all(), 4)
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
    paginate_by = 2
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


class BookedPerformanceByUserListView(LoginRequiredMixin,generic.ListView):
    model = PerformanceInstance
    template_name = 'theater/user_booked_performance.html'
    paginate_by = 4

    def get_queryset(self):
        return PerformanceInstance.objects.filter(viewer=self.request.user)

class BookedPerformanceByUserDelailView(LoginRequiredMixin, generic.DetailView):
    model = PerformanceInstance
    template_name = 'theater/user_performances.html'


class BookByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = PerformanceInstance
    fields = ('performance','performance_date',)
    success_url = reverse_lazy('my-booked')
    template_name = 'theater/user_performance_form.html'

    def form_valid(self, form):
        form.instance.viewer = self.request.user
        form.instance.status = _('not available')
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        performance_id = self.request.Get.get('performance_id')
        if performance_id:
            initial['performance'] = performance_id
        return initial
 
@login_required
def performance_attender(request, pi_id):
    performance = get_object_or_404(PerformanceInstance, id=pi_id)
    viewer = request.user

    viewers = []
    for view in performance.viewer.all():
        viewers.append(view)

    if viewer not in viewers and performance.ticket >= len(viewers)+1:
        performance.viewer.add(viewer)
        performance.save()
        messages.success(request, _('you have successfully booked'))

    else:
        messages.warning(request, _('there are no seats in the performance or you have already booked'))

    if len(viewers)+1 == performance.ticket:
        performance.status = 'not available'
        performance.save()

    return redirect ('my-booked')    

@login_required
def performance_cancel(request, pi_id):
    performance = get_object_or_404(PerformanceInstance, id=pi_id)
    viewer = request.user
    viewers = []
    for view in performance.viewer.all():
        viewers.append(view)
    if performance.status == 'not available':
        performance.viewer.remove(viewer)
        performance.status = 'available'
        performance.save()
        messages.success(request, _('your reservation has been successfully cancelled'))
    return redirect ('performances')
