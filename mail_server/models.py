# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Label(models.Model):
    label_id = models.CharField(max_length=50, null = True, blank = True)
    name = models.CharField(max_length=200, null = True, blank = True)
    def __unicode__(self):
        return self.name
        
class Template(models.Model):
    name=models.CharField(max_length=200, null = True, blank = True)
    content=models.TextField(max_length=10000, null = True, blank = True)
    def __unicode__(self):
        return self.name