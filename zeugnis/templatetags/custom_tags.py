from django import template

register = template.Library()

@register.filter(name='custom_range')
def custom_range(value):
    if value is None:
        return []
    return range(1, int(value) + 1)

@register.filter(name='to_stars')
def to_stars(avg_grade):
    if avg_grade is None:
        return 0
    if avg_grade <= 1.0:
        return 5
    elif avg_grade <= 2.0:
        return 4
    elif avg_grade <= 3.0:
        return 3
    elif avg_grade <= 4.0:
        return 2
    else:
        return 1
