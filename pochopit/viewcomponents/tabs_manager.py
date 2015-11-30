from django.core.handlers.wsgi import WSGIRequest
from pochopit.viewcomponents.tab import Tab


class TabsManager:
    request = None

    def __init__(self, request: WSGIRequest, active_tab: str):
        self.request = request
        self.items = []
        self.active_tab = active_tab
        if self.request.method == 'GET' and 'active_tab' in self.request.GET:
            self.active_tab = self.request.GET['active_tab']

    def add_tab(self, tab: Tab):
        self.items.append(tab)

    def add_tab_group(self, tab_group):
        self.items += tab_group.get_items()

    def get_tabs(self):
        for tab in self.items:
            if tab.isTabGroup:
                for action_button in tab.action_buttons:
                    action_button['is_active'] = action_button['shortName'] == self.active_tab
            else:
                tab.set_active(tab.shortName == self.active_tab)

        return self.items
