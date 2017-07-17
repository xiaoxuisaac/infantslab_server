# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class Label(models.Model):
    label_id = models.CharField(max_length=50, unique = True,  null = True, blank = True)
    name = models.CharField(max_length=200, null = True, blank = True)
    def __unicode__(self):
        return self.name
        
class Template(models.Model):
    name = models.CharField(max_length=200, null = True, blank = True)
    content = models.TextField(max_length=10000, null = True, blank = True)
    thread_id = models.CharField(max_length=200, unique = True, null = True, blank = True)
    def __unicode__(self):
        return self.name
        
        
class Email(models.Model):
    email=models.CharField(max_length=200, null = True, blank = True)
    subject=models.CharField(max_length=400, null = True, blank = True)
#    content=models.TextField(max_length=10000, null = True, blank = True)
    content = tinymce_models.HTMLField(null = True)
    labels = models.ManyToManyField(Label,blank=True,related_name='emails')
    template = models.ForeignKey(Template,blank=True,null = True, related_name='emails')
    family_data=models.TextField(max_length=5000, null = True, blank = True)
    
    def __unicode__(self):
        return self.subject 
        
