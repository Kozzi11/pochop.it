from django.core.urlresolvers import reverse
from django.template import loader

from _components.models.Component import Component
from _courses.models import ComponentData


class HTMLComponent(Component):

    def __init__(self, component_data: ComponentData):
        super().__init__()
        if component_data.type != ComponentData.TYPE_HTML:
            raise ValueError('ComponentData.type must be equal to HTML!')

        self.component_data = component_data

    def render_content(self) -> str:
        content = 'test'
        return loader.render_to_string('_components/html_content.html', {'content': content})

    def get_settings_url(self) -> str:
        return reverse('component_html', args=(self.component_data.id,))

    def get_css_url(self) -> str:
        pass

    def get_js_url(self) -> str:
        pass
