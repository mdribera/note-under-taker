from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from .models import Note, Label

class IndexView(generic.ListView):
  template_name = 'notes/index.html'
  context_object_name = 'latest_notes_list'

  def get_queryset(self):
    """ Return the last five notes """
    label_param = self.request.GET.get('label')
    if label_param is None:
      notes = Note.objects.all()
    else:
      label = get_object_or_404(Label, text=label_param)
      notes = label.notes

    return notes.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Note
  template_name = 'notes/detail.html'

  def get_queryset(self):
    """ Exclude notes that haven't been published yet """
    return Note.objects.filter(pub_date__lte=timezone.now())
