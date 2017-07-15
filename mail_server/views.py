# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from forms import EmailForm, LabelForm, TemplateForm
from django.core.mail import send_mail
from models import *

# Create your views here.
@csrf_exempt
def gen_email(request):
    if request.method == 'POST':
        
        try:
            data_web = request.POST
            form = email_from_template(data_web)
            return render(request,'email.html',{'form':form,'template_form': template_form})
        except:
            pass
    form = EmailForm()
    template_form = TemplateForm()
    return render(request,'email.html',{'form':form,'template_form': template_form})
    
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
            
def update(request):
    pass
    
def email_from_template(data_web, content_only = False):
    subject = "A New Study for [name of kid] from UChicago Center for Early Childhood Research"    
    data = {'test':'test'}
    try: 
        data['email'] = data_web["Email"]
    except: 
        data['email'] = ''
    
    try: 
        data['child_firs_name'] = data_web['child_name'].split(" ")[0].strip()
    except: 
        data['child_firs_name'] = '[name of kid]'
    
    try: 
        data['parent1_first_name'] = data_web['Parent 1'][0]
    except: 
        data['parent1_first_name'] = ''
    
    try: 
        data['parent2_first_name'] =data_web['Parent 1'][0]
    except: 
        data['parent2_first_name'] = ''
    
    try: 
        data['template'] = data_web["template"]
    except: 
        data['template'] = ''
    
    try: 
        data['labels'] = data_web["labels"]
    except: 
        data['labels'] = []
    
    try: 
        data['researcher'] = data_web["researcher"]
    except: 
        data['researcher'] = []
            
    template = Template.filter(name = data['tempalte'])
    if template.count() > 0:
        content = template[0].content
    else:
        content = ''
    
    #replace [name of kid]
    content = content.replace("[name of kid]", data['child_first_name'])
    subject = subject.repalce('[name of kid]', data['child_firs_name'])
    
    #replace '[parent's name]'
    if data['parent1_first_name'] != '':
        data['parent_first_name'] = data['parent1_first_name']
    elif data['parent2_first_name'] != '':
        data['parent_first_name'] = data['parent2_first_name']
    else:
        data['parent_first_name'] = '[parent\'s name]'
        
    content = content.repalce('[parent\'s name]', data['parent_first_name'])
    
    
    #replace [Your Name]
    content = content.repalce('[Your Name]', data['researcher'])
    
    if content_only:
        return content
    else:
        return  EmailForm({'email' : data['email'], 'subject' : subject, 'content' : content,
                            'template': data['tempalte'], 'labels' : data['labels']})

    
