from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic


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
