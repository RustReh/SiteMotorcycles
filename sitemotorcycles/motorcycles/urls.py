from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', cache_page(30)(views.MotorcyclesHome.as_view()), name='home'),  # http://127.0.0.1:8000
    path('post/<slug:post_slug>/', views.ShowMotorcycle.as_view(), name='post'),
    path('kind/<slug:kind_slug>/', views.MotorcycleKind.as_view(), name='kind'),
    path('type/<slug:type_slug>/', views.ShowEngineType.as_view(), name='type'),
    path('favorite/', views.FavoriteBikes.as_view(), name='favorite'),
    path('addpublication/', views.AddPublication.as_view(), name='addpublication'),
    path('edit/<slug:slug>/', views.UpdatePublication.as_view(), name='edit'),
    path('createorder/', views.AddToOrdersView.as_view(), name='create_order'),
    path('myorders/', views.MyOrdersView.as_view(), name='myorders'),
]
