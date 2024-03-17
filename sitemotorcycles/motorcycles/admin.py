from django.contrib import admin


from .models import Motorcycles, KindOfMotorcycle, EngineType


@admin.register(Motorcycles)
class MotorcyclesAdmin(admin.ModelAdmin):
    fields = ['photo', 'brand', 'bike_model', 'slug', 'description', 'kind', 'type', 'is_published']
    ordering = ['time_create', 'slug']
    list_display_links = ('brand', 'bike_model',)
    prepopulated_fields = {"slug": ("brand", 'bike_model' )}
    list_display = ('photo', 'brand', 'bike_model', 'kind', 'type', 'is_published')
    list_editable = ('is_published',)
    list_per_page = 5


@admin.register(KindOfMotorcycle)
class KindAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo_kind')
    list_display_links = ('id', 'name', 'photo_kind')
    ordering = ['id']


@admin.register(EngineType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'photo_engine')
    list_display_links = ('id', 'type', 'photo_engine')