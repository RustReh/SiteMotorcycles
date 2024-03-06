from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.MotorcyclesHome.as_view(), name='home'),  # http://127.0.0.1:8000
    path('post/<slug:post_slug>/', views.ShowMotorcycle.as_view(), name='post'),
    path('kind/<slug:kind_slug>/', views.MotorcycleKind.as_view(), name='kind'),
    path('type/<slug:type_slug>/', views.EngineType.as_view(), name='type'),
]
