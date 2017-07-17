# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from forms import EmailForm, LabelForm, TemplateForm, LabelUpdateForm, NewTemplateForm, AllTemplatesForm, EmailSettingForm
from django.core.mail import send_mail
from models import *
import json
import base64
import re

IGNORE_LABELS = ['CATEGORY_FORUMS', 'CATEGORY_PERSONAL', 'UNREAD', 'UNREAD',
'SPAM', 'DRAFT', 'CATEGORY_PROMOTIONS', 'TRASH', 'INBOX', 'SENT', 'CHAT',
'CATEGORY_UPDATES', 'IMPORTANT','CATEGORY_SOCIAL']

PARENT_NAME = ['[Parent name]','[parent name]', '[Parent\'s name]', '[parent\'s name]', '[parent&#39;s name]']

# Create your views here.
@csrf_exempt
def gen_email(request):
    if request.method == 'POST':
        try:
            data_web = request.POST
            form = email_from_template(data_web)
            return render(request,'email.html',{'form':form})
        except:
            pass
    form = EmailForm()
    return render(request,'email.html',{'form':form})
    
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail(
                    data['subject'],
                    data['content'],
                    'dibslab@gmail.com',
                    ['xiaoxuisaac@gmail.com'],
                    fail_silently=False,
                    )
            except:
                template_form = TemplateForm(request.POST)
                return render(request,'email.html',{'form':form, 'template_form' : template_form, 'message': 'Failed to Send to the Recipient!'})
            return render(request,'email_success.html',{'email' : data['email']})
        raise Http404
         
         
@csrf_exempt   
def update_labels(request):
    if request.method == 'POST':
        form = LabelUpdateForm(request.POST)
        if form.is_valid():
            labels = json.loads(form.cleaned_data['labels'])
            ids = []
            for label in labels:
                l, created = Label.objects.get_or_create(label_id = label['id'])
                l.name = label['name']
                if l.name not in IGNORE_LABELS:
                    l.save()
                    ids.append(label['id'])
                else:
                    l.delete()
            for l in Label.objects.all():
                if l.label_id not in ids:
                    l.delete()
        return HttpResponse("content")
    
def email_from_template(data_web, content_only = False):
    subject = "A New Study for [name of kid] from UChicago Center for Early Childhood Research"    
    data = {}
    try: 
        data['email'] = data_web["Email"]
    except: 
        data['email'] = ''
    
    try: 
        data['child_first_name'] = data_web['child_name'].split(" ")[0].strip()
    except: 
        data['child_first_name'] = '[name of kid]'
    
    try: 
        data['parent1_first_name'] = data_web['Parent 1'].split(" ")[0].strip()
    except: 
        data['parent1_first_name'] = ''
    
    try: 
        data['parent2_first_name'] =data_web['Parent 2'].split(" ")[0].strip()
    except: 
        data['parent2_first_name'] = ''
    
    try: 
        data['template'] = data_web["template"]
    except: 
        data['template'] = ''
    
    try: 
        data['labels'] = data_web["labels"]
    except: 
        data['labels'] = ''
    
    try: 
        data['researcher'] = data_web["researcher"]
        if data['researcher'] == "":
            data['researcher'] = "[Your Name]"
    except: 
        data['researcher'] = '[Your Name]'
            
    template = Template.objects.filter(name = data['template'])
    if template.count() > 0:
        template = template[0]
        content = template.content
    else:
        content = ''
        template = None
        
    #replace [name of kid]
    content = content.replace("[name of kid]", data['child_first_name'])
    subject = subject.replace('[name of kid]', data['child_first_name'])
    
    #replace '[parent's name]'
    if data['parent1_first_name'] != '':
        data['parent_first_name'] = data['parent1_first_name']
    elif data['parent2_first_name'] != '':
        data['parent_first_name'] = data['parent2_first_name']
    else:
        data['parent_first_name'] = '[parent\'s name]'
    
    for parent_name in PARENT_NAME:
        content = content.replace(parent_name, data['parent_first_name'])
    
    
    #replace [Your Name]
    content = content.replace('[Your Name]', data['researcher'])
    labels = []
    for l in data['labels'].split(','):
        ls = Label.objects.filter(name = l)
        if ls.count() > 0:
            labels.append(ls[0])
    
    if content_only:
        return content
    else:
        email = Email(email = data['email'], subject = subject, content = content, template = template, family_data = json.dumps(data_web))
        email.save()
        for l in labels:
            email.labels.add(l)
        form = EmailForm(instance = email)
        return form
        return  EmailForm({'email' : data['email'], 'subject' : subject, 'content' : content,
                            'template': template, 'labels' : labels})

def update_content_from_template(request):
    if request.method == 'POST':
        form = EmailSettingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            raise Http404
            
        try:
            data_web = data['family_data']
            data_web = json.loads(data_web)
        except:
            data_web = {}
        try:
            template = data['template']
        except:
            template = None
        try:
            data_web['template'] = template.name
        except:
            data_web['template'] = ''
            
        content = email_from_template(data_web, True)
        return HttpResponse(content)
    raise Http404
    
    
def get_label_id(request):
    if request.method == 'POST':
        form = EmailSettingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            raise Http404
            
        try:
            labels = data['labels']
        except:
            labels = []
        labels_id = ''
        for l in labels:
            labels_id = labels_id + l.label_id + ','
        if labels_id != '':
            labels_id = labels_id[:-1]
        return HttpResponse(labels_id)
    raise Http404
    
@csrf_exempt
def add_template(request):
    if request.method == 'POST':
        form = NewTemplateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            raise Http404
        subject = data['subject']
        content = data['content']
        #content = re.sub(r'(\n\s*)+(\n\s*)+\n+', '\n\n\n', content)
        #content = content.replace("\n\n\n", "[NEW_LINE_HERE]")
        #content = re.sub(r'\n\s*', '', content)
        #content = content.replace("[NEW_LINE_HERE]", "\n\n")
        content = content.split('<div class="gmail_quote">')[0]
        
        thread_id = data['thread_id']
        template, created= Template.objects.get_or_create(thread_id = thread_id)
        if created:
            template.name = subject
        template.content = content
        template.save()
        return HttpResponse('template added')
        
        
@csrf_exempt
def delete_old_templates(request):
    if request.method == 'POST':
        form = AllTemplatesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            raise Http404
        threads = json.loads(data['templates'])
        ids = []
        for thread in threads:
            ids.append(thread['id'])
        for t in Template.objects.all():
            if t.thread_id not in ids:
                t.delete()
        return HttpResponse('template updated')
    