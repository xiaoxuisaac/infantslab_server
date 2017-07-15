from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *
from django import forms
from django_select2.forms import (
     HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
     ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
     Select2Widget
 )
     

    
class LabelTagWidget(ModelSelect2MultipleWidget):
     model = Label
     queryset = Label.objects.all()
     search_fields = [
         'name',
     ]
         
      
class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels={
                 'name': _('Labels'),
                 }
        widgets = {
                'name':LabelTagWidget(attrs={'class':'form-control input-sm','data-placeholder':'Add Labels'}),
                }   
                
class TemplateWidget(ModelSelect2Widget):
      model=Template
      search_fields = [
           'name',
       ]               
                 
class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('name', )
        labels = {
                 'name': _('Template'),
                 }
        widgets = {
                'name': TemplateWidget(attrs={'class':'form-control', 'id':'template-select'})
                }
                
class EmailForm(forms.Form):
    email = forms.CharField(label=_("Recipient"),
                    widget=forms.TextInput(attrs={'type':'email', 'class':'form-control text-name', 'id' : "compose-to"}))
    subject = forms.CharField(label=_("Subject"),
                    widget=forms.TextInput(attrs={'class':'form-control text-name', 'id' : "compose-subject"}))
    content = forms.CharField(label=_("Content"),
                    widget=forms.Textarea(attrs={'class':'form-control text-name', 'id' : "compose-message"}))
    label = forms.CharField(label=_("Labels"), widget = LabelTagWidget(attrs={'class':'form-control input-sm','data-placeholder':'Add Labels', 'id':'label-select'}))
    
    template = forms.CharField(label=_("Template"), widget = TemplateWidget(attrs={'class':'form-control', 'id':'template-select'}))
    