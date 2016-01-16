from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag
def url_from_constant(app, constant_name, *args):
    mod = __import__(app)
    return reverse(getattr(mod.constants.URLS, constant_name), args=args)


@register.simple_tag
def urls_constant(app, constant_name):
    mod = __import__(app)
    return getattr(mod.constants.URLS, constant_name)

