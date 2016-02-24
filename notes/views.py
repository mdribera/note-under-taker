from django.shortcuts import render, get_object_or_404
from .models import Note

def index(request):
  latest_notes_list = Note.objects.order_by('-pub_date')[:5]
  context = { 'latest_notes_list': latest_notes_list }
  return render(request, 'notes/index.html', context)

def detail(request, note_id):
  note = get_object_or_404(Note, pk=note_id)
  return render(request, 'notes/detail.html', {'note': note})
