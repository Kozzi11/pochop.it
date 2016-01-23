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


@register.simple_tag
def has_permission(user, app, permission):
    mod = __import__(app)
    return user.has_permission(getattr(mod.constants.PERMISSION, permission))


@register.filter
def has_active_revision(model, user):
    return model.has_active_revision(user)
