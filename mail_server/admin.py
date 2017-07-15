# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name','content')
    
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name','label_id')
       
admin.site.register(Template,TemplateAdmin)
admin.site.register(Label,LabelAdmin)
