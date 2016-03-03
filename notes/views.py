from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from .models import Note, Label
from .forms import NoteForm


class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'latest_notes_list'

    def get_queryset(self):
        """
        Return the last five notes
        Filter using url params based on label and username
        """
        queryset = Note.objects.all()

        label_param = self.request.GET.get('label')
        user_param = self.request.GET.get('user')

        if label_param is not None:
            queryset = queryset.filter(labels__text=label_param)

        if user_param is not None:
            queryset = queryset.filter(author__username=user_param)

        return queryset.filter(
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'

    def get_queryset(self):
        """ Exclude notes that haven't been published yet """
        return Note.objects.filter(pub_date__lte=timezone.now())


class ComposeView(generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_compose_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.pub_date = timezone.now()
            note.author = request.user
            # import pdb
            # pdb.set_trace()
            note.save()
            return HttpResponseRedirect(
                reverse('notes:detail', kwargs={'pk': note.id}))


class EditView(generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('notes:detail', kwargs={'pk': self.object.id})


class DeleteView(generic.DeleteView):
    model = Note
    success_url = '/users/profile'
