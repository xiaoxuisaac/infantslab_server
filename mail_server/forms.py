from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *
from django import forms



class EmailForm(forms.Form):
    email = forms.CharField(label=_("Recipient"),
                    widget=forms.TextInput(attrs={'type':'email', 'class':'form-control text-name'}))
    subject = forms.CharField(label=_("Subject"),
                    widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    content = forms.CharField(label=_("Content"),
                    widget=forms.Textarea(attrs={'class':'form-control text-name'}))

