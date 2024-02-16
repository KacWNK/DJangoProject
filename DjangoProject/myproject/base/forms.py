from django.forms import ModelForm
from django import forms
from .models import Availability, User
from django.contrib.auth.forms import UserCreationForm


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = '__all__'

    def __init__(self, *args, user=None, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        if user:
            self.fields['user'].initial = user
            self.fields['user'].disabled = True

    def save(self, commit=True):
        instance = super(AvailabilityForm, self).save(commit=False)
        if not instance.user:
            raise ValueError("User must be set before saving the form.")
        if commit:
            instance.save()
        return instance

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email", "password1",'password2', "level", "age", "name"]
