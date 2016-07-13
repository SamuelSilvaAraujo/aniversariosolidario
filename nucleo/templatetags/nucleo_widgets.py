from django import template
from django.template import loader

register = template.Library()

@register.assignment_tag
def aniversario_panel(aniversario):
    return loader.render_to_string('nucleo/widgets/aniversario_panel.html', {
        'aniversario': aniversario
    })