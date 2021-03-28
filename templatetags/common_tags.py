from django import template

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
