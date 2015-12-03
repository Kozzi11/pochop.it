class Tab:
    title = ''
    url = '#'
    shortName = ''
    className = ''
    addBaddge = False
    baddgeNumber = 0
    isActive = False
    isTabGroup = False
    offset = 0
    action_buttons = []

    def __init__(self, title: str, url: str, short_name: str, is_active=False, buddge_number=None):
        self.title = title
        self.shortName = short_name
        self.url = url
        if is_active:
            self.className = 'active'
        self.isActive = is_active

        if buddge_number is not None:
            self.baddgeNumber = buddge_number
            self.addBaddge = True

        self.parrent = None
        self.action_buttons = []

    def set_active(self, active: bool):
        if active:
            self.className = 'active'
        else:
            self.className = ''
        self.isActive = active

    def add_action_button(self, url: str, glyphicon: str, short_name='', is_active=False, change_content=True,
                          js_after=''):
        self.action_buttons.append({'shortName': short_name, 'url': url,
                                    'glyphicon': 'glyphicon-' + glyphicon,
                                    'js_after': js_after,
                                    'is_active': is_active, 'change_content': change_content})
