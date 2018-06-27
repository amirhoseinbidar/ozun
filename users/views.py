# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.forms import forms
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from utils import account_activation_token , registerForm ,profileForm , check_user_exists_decorator, check_user_is_own
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from users.models import Email_auth , Profile
from django.core.exceptions import ValidationError



#method spliter  splite betwine diffrent  request methods
def method_splitter(request, GET=None, POST=None , **kwargs):
    if request.method == 'GET' and GET is not None:
        return GET(request,**kwargs)
    elif request.method == 'POST' and POST is not None:
        return POST(request,**kwargs)
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
        Profile(user =user).save()
        Email_auth.objects.filter(user = user).delete()
        login(request,user)

        return HttpResponseRedirect('/accounts/profile')
    else:
        return HttpResponse('Activation link is invalid!')


def profile_controller(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile/%s/' %(request.user.username))
    else:
        return HttpResponseRedirect('/accounts/login/')

@check_user_exists_decorator
def profile(request,username): 
    if check_user_is_own(request,username) :
        from datetime import date
        import time
        

        
        person = Profile.objects.get(user__username = username)
       
        try :
            deffrence = date.today() - person.brith_day
        except:
            deffrence = 0

        age_year = deffrence.days // (365.25)
        age_month = (deffrence.days- age_year *365.25)//(365.25/12)
        print(age_year,age_month)

        context = {
            'bio' : person.bio,
            'image': person.image,
            'name' : person.user.get_full_name(),
            'location': person.location,
            'age_year': age_year,
            'age_month': age_month,
        }
        
        return HttpResponse('hello this is your profile  , bio: %s'%(person.bio))         
    else:
        return HttpResponse('hello this is %s profile' % (username))


@check_user_exists_decorator
def profile_edit_GET(request,username): 
    if check_user_is_own(request, username):
        form  = profileForm()
        return render(request,'edit_profile.html',{'form':form})  
    else:
        return HttpResponseRedirect('accounts/%s/' %(username))


def profile_edit_POST(request,username):
    pass 

