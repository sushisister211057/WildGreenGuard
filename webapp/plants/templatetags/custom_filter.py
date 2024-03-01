from django import template

register = template.Library()

@register.filter(name="split")
def cut(value, delimiter):
    return value.split(delimiter)[0]
