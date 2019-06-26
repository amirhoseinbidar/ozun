from django import forms


class DataListTextInput(forms.widgets.Input):
    input_type = 'text'
    template_name = 'datalist.html'

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = list(choices)

    def get_context(self, name, value, attrs):
        attrs = self.set_attrs(attrs, name)
        context = super().get_context(name, value, attrs)
        context['widget']['options'] = self.choices
        return context

    def set_attrs(self, attrs, name):
        if not attrs:
            attrs = {}
        attrs['list'] = name + '-list'
        return attrs
