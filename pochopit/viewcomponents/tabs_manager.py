from django.core.handlers.wsgi import WSGIRequest
from pochopit.viewcomponents.tab import Tab


class TabsManager:
    request = None

    def __init__(self, request: WSGIRequest):
        self.request = request
        self.items = []

    def add_tab(self, tab: Tab):
        self.items.append(tab)

    def add_tab_group(self, tab_group):
        self.items += tab_group.get_items()

    def get_tabs(self):
        return self.items
