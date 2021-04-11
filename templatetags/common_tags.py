from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def to_verbose_name(value):
    return value._meta.verbose_name


@register.filter
def to_verbose_plural_name(value):
    return value._meta.verbose_name_plural


@register.filter
def to_model_verbose_name(value):
    return value.model._meta.verbose_name


@register.filter(name='abs')
def abs_filter(value):
    return abs(value)
