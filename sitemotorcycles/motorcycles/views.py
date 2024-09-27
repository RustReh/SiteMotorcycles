import csv
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

from .forms import AddPublicationForm, AddToFavForm, AddToOrderForm
from .models import Motorcycles, EngineType, Favorite, Order
from .permissions import IsEditorOrReadOnly
from .serializers import BikeSerializer, OrderSerializer
from .tasks import send_mails, send_notification
from .utils import DataMixin


class MotorcyclesHome(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'publications'
    title_page = 'Главная страница'
    kind_selected = 0

    def get_queryset(self):
        return Motorcycles.published.all().select_related('kind')


class ShowMotorcycle(DataMixin, FormMixin, DetailView):
    template_name = 'motorcycles/post.html'
    form_class = AddToFavForm
    slug_url_kwarg = 'post_slug'
    context_object_name = 'publication'

    def post(self, request, *args, **kwargs):
        user = request.user
        motorcycles = self.get_object()

        if Favorite.objects.filter(user=user, motorcycles=motorcycles).exists():
            f = Favorite.objects.filter(motorcycles=motorcycles)
            f.delete()

        else:
            favorite = Favorite(user=user, motorcycles=motorcycles)
            favorite.save()
            send_mails(user, favorite.motorcycles)

        return redirect('post', self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['publication'].brand)

    def get_object(self, queryset=None):
        return get_object_or_404(Motorcycles.published, slug=self.kwargs[self.slug_url_kwarg])

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
        return Motorcycles.published.filter(type__slug=self.kwargs['type_slug']).select_related('kind')


class MotorcycleKind(DataMixin, ListView):
    template_name = 'motorcycles/index.html'
    context_object_name = 'publications'
    allow_empty = False

    def get_queryset(self):
        return Motorcycles.published.filter(kind__slug=self.kwargs['kind_slug']).select_related('kind')

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

    def get_user_pk(self):
        return self.request.user.pk

    def get_queryset(self):
        return Favorite.objects.filter(user=self.get_user_pk())


class AddPublication(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPublicationForm
    template_name = 'motorcycles/add_publication.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление публикации'
    permission_required = 'motorcycles.add_motorcycles'


class UpdatePublication(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Motorcycles
    fields = ['brand', 'bike_model', 'photo', 'is_published', 'description', 'kind', 'type']
    template_name = 'motorcycles/add_publication.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'motorcycles.change_motorcycles'


class AddToOrdersView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddToOrderForm
    template_name = 'motorcycles/create_order.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.create(user=user,
                                     needed_quantity=self.request.POST.get('needed_quantity'),
                                     motorcycle=Motorcycles.objects.get(pk=self.request.POST.get('motorcycle'))
                                     )
        order.save()
        return redirect('home')

    def get_user_pk(self):
        return self.request.user.pk

    def get_initial(self):
        initial = super(AddToOrdersView, self).get_initial()
        initial['user'] = self.get_user_pk()
        return initial

class MyOrdersView(DataMixin, ListView):
    template_name = 'motorcycles/orders.html'
    context_object_name = 'orders'
    title_page = 'My Orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)




# DRF classes here
class MotorcyclesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Motorcycles.published.all()
    serializer_class = BikeSerializer


class MotorcyclesAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Motorcycles.objects.all()
    serializer_class = BikeSerializer
    permission_classes = (IsEditorOrReadOnly, )


class MotorcyclesAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Motorcycles.objects.all()
    serializer_class = BikeSerializer
    permission_classes = (IsEditorOrReadOnly, )


class OrderCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        send_notification(user=self.request.user, order=self.request.data)


class OrderViewAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

