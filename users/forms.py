from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError

from .models import User


class UserCacheMixin:
    user_cache = None


class LogInForm(UserCacheMixin, forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError("You entered an invalid username.")

        self.user_cache = user

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError("You entered an invalid password.")

        return password


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if user:
            raise ValidationError("You can not use this username.")

        return username
