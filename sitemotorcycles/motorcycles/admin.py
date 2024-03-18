from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Motorcycles, KindOfMotorcycle, EngineType


@admin.register(Motorcycles)
class MotorcyclesAdmin(admin.ModelAdmin):
    fields = ['post_photo', 'photo', 'brand', 'bike_model', 'slug', 'description', 'kind', 'type', 'is_published']
    readonly_fields = ['post_photo']
    ordering = ['time_create', 'slug']
    list_display_links = ('brand', 'bike_model',)
    prepopulated_fields = {"slug": ("brand", 'bike_model' )}
    list_display = ('post_photo', 'brand', 'bike_model', 'kind', 'type', 'is_published')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['brand__startswith', 'kind__name']
    list_filter = ['kind__name', 'is_published']

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, motorcycles: Motorcycles):
        if motorcycles.photo:
            return mark_safe(f"<img src='{motorcycles.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Motorcycles.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Motorcycles.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(KindOfMotorcycle)
class KindAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo_kind')
    list_display_links = ('id', 'name', 'photo_kind')
    ordering = ['id']


@admin.register(EngineType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'photo_engine')
    list_display_links = ('id', 'type', 'photo_engine')