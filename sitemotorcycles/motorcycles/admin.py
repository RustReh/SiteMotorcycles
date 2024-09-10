from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Motorcycles, KindOfMotorcycle, EngineType, Menu, Order


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
            return mark_safe(f"<img src='{motorcycles.photo.url}' width=100>")
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
    fields = ['kind_photo', 'name', 'photo_kind', 'slug']
    readonly_fields = ['kind_photo']
    list_display = ('kind_photo', 'id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['id']

    def kind_photo(self, kind: KindOfMotorcycle):
        if kind.photo_kind:
            return mark_safe(f"<img src='{kind.photo_kind.url}' width=100>")
        return "Без фото"


@admin.register(EngineType)
class TypeAdmin(admin.ModelAdmin):
    fields = ['eng_photo', 'type', 'photo_engine', 'slug']
    list_display = ('photo_engine', 'id', 'type', 'slug')
    readonly_fields = ['eng_photo']
    list_display_links = ('id', 'type')

    def eng_photo(self, eng: EngineType):
        if eng.photo_engine:
            return mark_safe(f"<img src='{eng.photo_engine.url}' width=100>")
        return "Без фото"


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['title', 'url', 'position']
    list_display = ('title', 'url', 'position')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'needed_quantity', 'motorcycle')
    readonly_fields = ['time_create']
