from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from .models import Note

class IndexView(generic.ListView):
  template_name = 'notes/index.html'
  context_object_name = 'latest_notes_list'

  def get_queryset(self):
    """ Return the last five notes """
    return Note.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Note
  template_name = 'notes/detail.html'

  def get_queryset(self):
    """ Exclude notes that haven't been published yet """
    return Note.objects.filter(pub_date__lte=timezone.now())
