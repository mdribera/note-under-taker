from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Note

class IndexView(generic.ListView):
  template_name = 'notes/index.html'
  context_object_name = 'latest_notes_list'
  latest_notes_list = Note.objects.order_by('-pub_date')[:5]

  def get_queryset(self):
    """Return the last five notes"""
    return Note.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Note
  template_name = 'notes/detail.html'
