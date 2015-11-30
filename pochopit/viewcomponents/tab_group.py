from pochopit.viewcomponents.tab import Tab


class TabGroup:
    _uid = 0
    isTabGroup = True
    offset = 0
    uid = 0
    action_buttons = []

    def __init__(self, title: str, expand=False, buddge_number=None):
        self.title = title
        self.expand = expand
        self.buddge_number = buddge_number
        if buddge_number is not None:
            self.baddgeNumber = buddge_number
            self.addBaddge = True

        self.action_buttons = []
        self.parrent = None
        self.items = []
        self.items.append(self)
        self.uid = TabGroup._uid
        TabGroup._uid += 1

    def get_uid(self) -> int:
        return self.uid

    def add_tab(self, tab: Tab):
        tab.parrent = self
        tab.offset += 1
        self.items.append(tab)

    def add_tab_group(self, tab_group):
        tab_group.parrent = self
        for item in tab_group.get_items():
            item.offset += 1
            self.items.append(item)

    def add_action_button(self, short_name: str, url: str, glyphicon: str):
        self.action_buttons.append({'shortName': short_name, 'url': url, 'glyphicon': 'glyphicon-' + glyphicon})

    def get_items(self):
        return self.items