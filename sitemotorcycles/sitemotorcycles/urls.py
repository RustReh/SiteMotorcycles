"""
URL configuration for sitemotorcycles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from motorcycles.views import *

router = routers.DefaultRouter()
router.register(r'motorcycles', MotorcyclesViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('motorcycles.urls')),
                  path('api/v1/', include(router.urls)),
                  path('api/v1/bike/<int:pk>/', MotorcyclesAPIUpdate.as_view()),
                  path('api/v1/bikedelete/<int:pk>/', MotorcyclesAPIDestroy.as_view()),
                  path('api/v1/createorder/', OrderCreateAPIView.as_view()),
                  path('api/v1/createorder/<int:pk>/', OrderCreateAPIView.as_view()),
                  path('api/v1/order/', OrderViewAPIView.as_view()),
                  path('users/', include('users.urls', namespace="users")),
                  path('social-auth/', include('social_django.urls', namespace='social')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Мотоциклы'