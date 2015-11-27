from _components.models import Component
from _components.models.HTMLComponent import HTMLComponent
from _courses.models import ComponentData


class ComoponentBuilder:
    pass

    @staticmethod
    def prepare_component(component_data: ComponentData)->Component:
        switcher = {
            ComponentData.TYPE_HTML: HTMLComponent,
        }
        return switcher.get(component_data.type)(component_data)
