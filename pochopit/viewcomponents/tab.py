

class Tab:
    name = ''
    url = '#'
    className = ''
    addBaddge = False
    baddgeNumber = 0

    def __init__(self, name: str, url: str, is_active: bool, buddge_number=None):
        self.name = name
        self.url = url
        if is_active:
            self.className = 'active'

        if buddge_number is not None:
            self.baddgeNumber = buddge_number
            self.addBaddge = True