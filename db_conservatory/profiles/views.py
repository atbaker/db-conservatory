from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import RegistrationForm

class UserCreate(FormView):
    form_class = RegistrationForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = User.objects.create_user(username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password1'])
        
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
            # Come back and add more logic later
        
        return redirect(self.success_url) 

