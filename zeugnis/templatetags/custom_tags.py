from django import template
import math

register = template.Library()

@register.filter(name='custom_range')
def custom_range(value, arg=None):
    if arg is None:
        start, end = 1, value
    else:
        start, end = value, arg
    return range(start, end + 1)

@register.filter(name='add')
def add(value, arg):
    return value + arg

@register.filter(name='to_stars')
def to_stars(avg_grade):
    if avg_grade is None:
        return 0
    if avg_grade <= 1.0:
        return 5
    elif avg_grade <= 1.5:
        return 4.5
    elif avg_grade <= 2.0:
        return 4
    elif avg_grade <= 2.5:
        return 3.5
    elif avg_grade <= 3.0:
        return 3
    elif avg_grade <= 3.5:
        return 2.5
    elif avg_grade <= 4.0:
        return 2
    elif avg_grade <= 4.5:
        return 1.5
    else:
        return 1


@register.filter(name='custom_get')
def custom_get(dictionary, key):
    return dictionary.get(key, 0.0)  