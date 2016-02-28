from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
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


def signup(request):
    """ A user is already signed in """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    """ If this is a POST request we need to process the form data """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        """ If it's a GET request (or any other method) we'll create a blank form """
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
