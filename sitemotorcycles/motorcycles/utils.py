

class DataMixin:
    title_page = None
    kind_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.kind_selected is not None:
            self.extra_context['kind_selected'] = self.kind_selected


    def get_mixin_context(self, context, **kwargs):
        context['kind_selected'] = None
        context.update(kwargs)
        return context
