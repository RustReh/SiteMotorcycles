from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import AddPublicationForm, AddToFavForm
from .models import Motorcycles, EngineType, Favorite
from .utils import DataMixin


class MotorcyclesHome(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'publications'
    title_page = 'Главная страница'
    kind_selected = 0

    def get_queryset(self):
        return Motorcycles.objects.all().select_related('kind')


class ShowMotorcycle(DataMixin, FormMixin, DetailView):
    template_name = 'motorcycles/post.html'
    form_class = AddToFavForm
    slug_url_kwarg = 'post_slug'
    context_object_name = 'publication'

    def post(self, request, *args, **kwargs):
        # bike_pk = self.kwargs['pk']
        user = request.user
        motorcycles = Motorcycles.objects.get(slug=self.slug)
        favorite = Favorite(user=user, motorcycles=motorcycles)
        favorite.save()
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['publication'].brand)

    def get_object(self, queryset=None):
        return get_object_or_404(Motorcycles.objects.all(), slug=self.kwargs[self.slug_url_kwarg])

    def get_user_pk(self):
        return self.request.user.pk

    def get_initial(self):
        initial = super(ShowMotorcycle, self).get_initial()
        initial['motorcycles'] = self.object  # selected bike
        initial['user'] = self.get_user_pk()
        return initial


class ShowEngineType(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'publications'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = EngineType.objects.get(slug=self.kwargs['type_slug'])
        return self.get_mixin_context(context, title='Тег: ' + types.type)

    def get_queryset(self):
        return Motorcycles.objects.all().filter(type__slug=self.kwargs['type_slug']).select_related('kind')


class MotorcycleKind(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'publications'
    allow_empty = False

    def get_queryset(self):
        return Motorcycles.objects.all().filter(kind__slug=self.kwargs['kind_slug']).select_related('kind')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kind = context['publications'][0].kind
        return self.get_mixin_context(context,
                                      title='Класс - ' + kind.name,
                                      kind__slug=kind.pk,
                                      )


class FavoriteBikes(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'motorcycles/favorite_bikes.html'
    context_object_name = 'fav_publications'
    title_page = 'Избранные мотоциклы'
    kind_selected = 0

    def get_queryset(self):
        pass


class AddPublication(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPublicationForm
    template_name = 'motorcycles/add_publication.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление публикации'


class UpdatePublication(DataMixin, UpdateView):
    model = Motorcycles
    fields = ['brand', 'bike_model', 'photo', 'description', 'kind', 'type']
    template_name = 'motorcycles/add_publication.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

