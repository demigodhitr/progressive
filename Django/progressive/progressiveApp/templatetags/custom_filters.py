# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def format_number(card_number):
    card_number = ''.join(card_number.split()) 
    formatted_number = ' '.join(card_number[i:i+4] for i in range(0, len(card_number), 4))
    return formatted_number


@register.filter
def new_formatter(number):
    number = ''.join(number.split()) 
    new_formatted = ' - '.join(number[i:i+4] for i in range(0, len(number), 4))
    return new_formatted