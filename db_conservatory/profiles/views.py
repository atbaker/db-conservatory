from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from .forms import LoginForm

class UserCreate(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'password']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        User.objects.create_user(username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password'])
        return redirect(self.success_url)   

class UserLogin(FormView):
    template_name = 'auth/login_form.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']


        import pdb; pdb.set_trace()