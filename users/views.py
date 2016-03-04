from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from notes.models import Note


class SignupView(generic.View):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(
                request,
                self.template_name,
                {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = authenticate(username=username, password=password,)
            login(request, new_user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ProfileView(generic.DetailView):
    model = User
    template_name = 'users/profile.html'

    def get(self, request):
        notes = Note.objects.filter(author=request.user).order_by('-pub_date')
        return render(request, self.template_name, {'notes': notes})
