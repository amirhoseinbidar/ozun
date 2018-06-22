# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.forms import forms
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from users import forms
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from token import account_activation_token 
from forms import registerForm
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from users.models import email_auth



# Create your views here.

#method spliter  splite betwine diffrent  request methods
def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    else:
        raise Http404

#this function run in first request to register url 
def register_GET(request):
    form = registerForm()
    return render(request,'register.html',{'form':form})

def register_POST(request):
    form = registerForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email_auth().create_record(user)

        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponseRedirect('/accounts/register/successfully')
    else: 
        print(form.error_messages) 
        return render(request,'register.html',{'form': form})

    #should make a random string 
    #then send it to the email_auth table with his/her username,password and email and add_date and remove_date
    #and send random string to his email  
    #(done in register_form)
    ###############
    #and when he is opening /accounts/email_auth/RANDOM_STRING 
    #then send his name as a user in users database
    #(done in active)
    ###############
    #TODO:make a function every 10 minute check email_auth table 
    #if remove_date of a recorde passed remove this recorde


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except Exception  , e :
        print(e)
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)

        return HttpResponseRedirect('/accounts/register/successfully')
    else:
        return HttpResponse('Activation link is invalid!')

    
