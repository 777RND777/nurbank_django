from django import forms
from django.conf import settings
from django.forms import ValidationError

from . import models


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['value']

    def clean_value(self):
        value = self.cleaned_data['value']
        if value < 1:
            raise ValidationError("Please enter positive value.")
        if value > settings.ONE_APPLICATION_LIMIT:
            raise ValidationError(f"You entered too big number. Limit is {settings.ONE_APPLICATION_LIMIT}.")

        return value


class PaymentForm(ApplicationForm):
    def clean_value(self):
        value = super().clean_value()
        return -value
