from django.core.urlresolvers import reverse


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

    def __init__(self, title: str, viewname: str, params=None, is_active=False, buddge_number=None):
        self.title = title
        self.shortName = viewname.split('_')[-1]
        self.url = reverse(viewname, args=params)
        if is_active:
            self.className = 'active'
        self.isActive = is_active

        if buddge_number is not None:
            self.baddgeNumber = buddge_number
            self.addBaddge = True

        self.parrent = None
