from django.contrib.auth import authenticate, login
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                import pdb; pdb.set_trace()
            else:
                raise forms.ValidationError("This user account has been deactivated")
        else:
            raise forms.ValidationError("This username or password is invalid")
