from django import template

from notes.models import Label

register = template.Library()

@register.inclusion_tag('notes/label_list_nav.html')
def label_list_nav():
	return {'labels': Label.objects.all()}