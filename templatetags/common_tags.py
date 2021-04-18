from django import template

register = template.Library()


@register.filter
def to_verbose_name(value):
    return value._meta.verbose_name


@register.filter
def to_verbose_plural_name(value):
    return value._meta.verbose_name_plural


@register.filter(is_safe=True)
def to_model_verbose_name(value):
    return value.model._meta.verbose_name


@register.filter(name='abs', is_safe=True)
def abs_filter(value):
    return abs(value)


@register.simple_tag
def percent(value, maximum):
    return (value / maximum) * 100
