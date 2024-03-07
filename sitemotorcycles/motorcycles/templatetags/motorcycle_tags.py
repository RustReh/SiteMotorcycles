from django import template
from django.db.models import Count

from ..models import KindOfMotorcycle, EngineType, Menu

register = template.Library()


@register.inclusion_tag('motorcycles/menu_top.html')
def show_top_menu():
    menu_items = Menu.objects.all()
    return {
        "menu_items": menu_items,
    }


@register.inclusion_tag('motorcycles/list_kinds.html')
def show_kind(kind_selected=0):
    kinds = KindOfMotorcycle.objects.all()
    return {'kinds': kinds, } #'kind_selected': kind_selected


@register.inclusion_tag('motorcycles/list_eng_type.html')
def show_all_types(type_selected=0):
    types = EngineType.objects.all()
    return {'types': types, } #'type_selected': type_selected
