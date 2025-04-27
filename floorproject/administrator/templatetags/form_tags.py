# administrator/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """Ajoute une classe CSS à un widget de formulaire"""
    return value.as_widget(attrs={"class": css_class})