from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Motorcycles
from .utils import DataMixin


class MotorcyclesHome(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    kind_selected = 0

    def get_queryset(self):
        return Motorcycles.objects.all().select_related('kind')


class ShowMotorcycle(DataMixin, DetailView):
    template_name = 'motorcycles/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Motorcycles.objects.all(), slug=self.kwargs[self.slug_url_kwarg])


class EngineType(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Motorcycles.objects.all().filter(cat__slug=self.kwargs['type_slug']).select_related("type")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kind = context['posts'][0].kind
        return self.get_mixin_context(context,
                                      title='Тип двигателя - ' + kind.name,
                                      cat_selected=kind.pk,
                                      )


class MotorcycleKind(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Motorcycles.objects.all().filter(cat__slug=self.kwargs['kind_slug']).select_related("kind")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kind = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Класс - ' + kind.name,
                                      cat_selected=kind.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
