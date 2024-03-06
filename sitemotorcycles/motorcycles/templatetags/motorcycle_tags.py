from django import template
from django.db.models import Count

from motorcycles.models import KindOfMotorcycle, EngineType


register = template.Library()


@register.inclusion_tag('motorcycles/list_kinds.html')
def show_kind(kind_selected=0):
    kinds = KindOfMotorcycle.objects.all().annotate(total=Count("posts")).filter(total__gt=0)
    return {'kinds': kinds, 'kind_selected': kind_selected}


@register.inclusion_tag('motorcycles/list_eng_type.html')
def show_all_types(type_selected=0):
    types = EngineType.objects.all().annotate(total=Count("posts")).filter(total__gt=0)
    return {'types': types, 'type_selected': type_selected}
