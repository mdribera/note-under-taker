from django import template

register = template.Library()

@register.inclusion_tag('notes/label_list.html')
def label_list(labels):
	return {'labels': labels}