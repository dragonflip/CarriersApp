"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

#class BootstrapAuthenticationForm(AuthenticationForm):
#    """Authentication form which uses boostrap CSS."""
#    #username = forms.CharField(max_length=254,
#    #                           widget=forms.TextInput({
#    #                               'class': 'form-control',
#    #                               'placeholder': 'User name'}))
#    email = forms.EmailField(widget=forms.EmailInput({
#                                   'class': 'form-control',
#                                   'placeholder': 'Email'}))
#    password = forms.CharField(widget=forms.PasswordInput({
#                                   'class': 'form-control',
#                                   'placeholder':'Password'}))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)

        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password = self.cleaned_data['password1']

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
 
        self.fields['username'].required = False 
        self.fields['password2'].required = False 

        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['email'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['placeholder'] = 'Електронна пошта'
        self.fields['email'].widget.attrs['autofocus'] = True

        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg mt-2'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введіть ім\'я'

        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-lg mt-2'
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введіть прізвище'

        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg mt-2'
        self.fields['password1'].widget.attrs['required'] = True
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'

        #self.fields['password2'].widget.attrs['class'] = 'form-control mt-2'
        #self.fields['password2'].widget.attrs['required'] = True
        #self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class CustomResetPassword(auth_views.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPassword, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['email'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['placeholder'] = 'Електронна пошта'
        self.fields['email'].widget.attrs['autofocus'] = True

class CustomSetPassword(auth_views.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPassword, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-lg mt-2'
        self.fields['new_password1'].widget.attrs['required'] = True
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Пароль'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-lg mt-2'
        self.fields['new_password2'].widget.attrs['required'] = True
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Підтвердження пароля'

