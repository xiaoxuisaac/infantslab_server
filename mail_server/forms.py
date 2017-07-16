from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *
from django import forms
from django.utils.encoding import force_text

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
                
class LabelUpdateForm(forms.Form):
    labels = forms.CharField(required=False,label="Text Name",max_length=100000,widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    
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
                
class EmailForm(forms.ModelForm):
    class Meta:
             model = Email
             fields = ['email','subject','content','labels','template','family_data']
    
             labels = {'email': _('Recipient'),
                'subject': _('Subject'),
                'content': _('Conetent'),
                'labels': _('Labels'),
                'template': _('Template')
                }
            
             widgets = {'email': forms.TextInput(attrs={'type':'email', 'class':'form-control text-name', 'id' : "compose-to"}),
                    'subject': forms.TextInput(attrs={'class':'form-control text-name', 'id' : "compose-subject"}),
                    'content': forms.Textarea(attrs={'class':'form-control text-name', 'id' : "compose-message"}),
                    'labels': LabelTagWidget(attrs={'class':'form-control input-sm','data-placeholder':'Add Labels', 'id':'label-select'}),
                    'template': TemplateWidget(attrs={'class':'form-control', 'id':'template-select'}),
                    'family_data': forms.TextInput(attrs={'class':'form-control text-name', 'id' : "compose-subject", 'style':'display:none;'}),
                    
                    }
            
class NewTemplateForm(forms.Form):
    subject = forms.CharField(required=False,label="Subject",max_length=500,widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    content = forms.CharField(required=False,label="Text Name",max_length=1000000,widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    thread_id = forms.CharField(required=False,label="Subject",max_length=500,widget=forms.TextInput(attrs={'class':'form-control text-name'}))
    
class AllTemplatesForm(forms.Form):
    templates = forms.CharField(required=False,label="Text Name",max_length=1000000,widget=forms.TextInput(attrs={'class':'form-control text-name'}))