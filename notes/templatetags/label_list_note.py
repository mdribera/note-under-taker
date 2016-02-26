from django import template

register = template.Library()

@register.inclusion_tag('notes/label_list_note.html')
def label_list_note(labels):
	return {'labels': labels}