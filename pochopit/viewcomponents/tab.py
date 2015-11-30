

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

    def set_active(self, active: bool):
        if active:
            self.className = 'active'
        else:
            self.className = ''
        self.isActive = active
