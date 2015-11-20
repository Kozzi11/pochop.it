from django.core.urlresolvers import reverse


class Tab:
    name = ''
    url = '#'
    shorName = ''
    className = ''
    addBaddge = False
    baddgeNumber = 0

    def __init__(self, name: str, viewname: str, params=None, is_active=False, buddge_number=None):
        self.name = name
        self.shortName = viewname.split('_')[-1]
        self.url = reverse(viewname, args=params)
        if is_active:
            self.className = 'active'

        if buddge_number is not None:
            self.baddgeNumber = buddge_number
            self.addBaddge = True
