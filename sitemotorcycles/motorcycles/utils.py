from .models import Menu

menu = Menu.objects.all()


class DataMixin:
    # paginate_by = 3
    title_page = None
    # kind_selected = None
    # extra_context = {}

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        # if self.kind_selected is not None:
        #     context['kind_selected'] = self.kind_selected

        # if "paginator" in context:
        #     context["page_range"] = context["paginator"].get_elided_page_range(context["page_obj"].number,
        #                                                                        on_each_side=2, on_ends=1)

        context.update(kwargs)

        # if 'menu' not in context:
        #     context['menu'] = menu

        return context
