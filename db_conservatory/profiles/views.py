from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView

class UserCreate(CreateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email', 'password']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.username = form.instance.email
        return super(UserCreate, self).form_valid(form)    
