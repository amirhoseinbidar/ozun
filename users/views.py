# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import forms
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from users.utils.checks import check_user_exists_decorator ,check_user_is_own
from users.utils.forms import registerForm ,  profileEditForm
from users.utils.token import TokenGenerator ,account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from users.models import Email_auth, Profile  , Country_city
from django.core.exceptions import ValidationError
from quizzes.forms import quiz_select_form

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
        #when record timeout in Email auth end we clear user and email auth so
        # if user cleared this function raise error  
    except :
        user = None
    
    if user is not None and account_activation_token.check_token(user, token) :
        user.is_active = True
        user.save()
        Profile(user =user).save()
        Email_auth.objects.get(user = user).delete()
        login(request,user)

        return HttpResponseRedirect('/accounts/profile')
    else:
        return HttpResponse('Activation link is invalid!')


def profile_controller(request):# after register  or login  page redirect to this function (specified in sitting)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile/%s/' %(request.user.pk))
    else:
        return HttpResponseRedirect('/accounts/login/')
        

@check_user_exists_decorator
def profile(request,pk,attr): 
    person = Profile.objects.get(user__pk = pk)
    from datetime import date
    from django.utils.crypto import get_random_string

    try :
        deffrence = date.today() - person.brith_day
        age_year = deffrence.days // (365.25)
        age_month = (deffrence.days- age_year *365.25)//(365.25/12)
    except:
        age_year = 0
        age_month = 0    
    
    context = {
        'domain': get_current_site(request).domain,
        'bio' : person.bio,
        'image': person.image.url,
        'name' : person.user.get_full_name(),
        'location': person.location,
        'age_year': int(age_year),
        'age_month': int(age_month),
        'username' : person.user.username,
    }
    

    if check_user_is_own(request, attr,pk):
        context['quiz_select_form']= quiz_select_form( {'token' : get_random_string(length=30)} )
        context['is_user_own']=  True
        return render(request,'profile.html',context)         
    else:
        context['is_user_own']=  False
        return render(request,'profile.html',context)

#Redirecting user to his profile is by his pk in the table of user 
@check_user_exists_decorator
def profile_edit_GET(request,pk,attr):
    if check_user_is_own(request,attr,pk):    
        person = Profile.objects.get(user__pk =pk)

        if person.location:
            provinc = person.location.county.province.pk
            county =  person.location.county.pk
            city = person.location.pk
        else:
            provinc = county = city = -1

        profileContext = {
            'first_name' : person.user.first_name,
            'last_name' : person.user.last_name,
            'bio': person.bio,
            'location': person.location,
            'brith_day' : person.brith_day,
            'provinces_field' :  provinc,
            'counties_field': county,
            'cities_field': city,
        }

        form  = profileEditForm(profileContext)
        
        context = {
            'form' : form,
            'image' : person.image.url,
           
        }

        return render(request,'edit_profile.html',context)  
    else:
        return HttpResponseRedirect('/accounts/profile/%s/' %(pk))

@check_user_exists_decorator
def profile_edit_POST(request,pk,attr):
    if check_user_is_own(request,attr,pk):
        person = Profile.objects.get(user__pk = pk)# user intered  info  saved in db
        form = profileEditForm(request.POST,request.FILES)

        

        if form.is_valid():
            user = form.save(commit = False)#user sended data but we dont deploy it to db(commit=False) 
             #TODO:this is insecure information should not store in db directly
            person.user.last_name = form.cleaned_data['last_name']
            person.user.first_name = form.cleaned_data['first_name']
            person.bio = user.bio
            person.brith_day = user.brith_day
            if form.cleaned_data['cities_field'] != '-1':
                person.location = Country_city.objects.get( pk = int(form.cleaned_data['cities_field']))
            else:
                person.location = None
            if user.image :
                person.image = user.image
                person.save()
                person.user.save()
            else:
                person.save()
                person.user.save()
            #TODO: maybe make a alert which say profile edited     
        else:
            return render(request,'edit_profile.html',{'form':form ,'image':person.image.url})
    return HttpResponseRedirect('/accounts/profile/%s/' %(pk))
