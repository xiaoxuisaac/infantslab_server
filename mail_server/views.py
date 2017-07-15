# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from forms import EmailForm, LabelForm, TemplateForm
from django.core.mail import send_mail

# Create your views here.
@csrf_exempt
def gen_email(request):
    if request.method == 'POST':
        
        try:
            form = EmailForm(request.POST)
            template_form = TemplateForm(request.POST)
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