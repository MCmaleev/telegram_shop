from django import template

register = template.Library()


def multiply(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return value * 1000


register.filter('multiply', multiply)
