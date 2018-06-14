# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.forms import forms
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from users import forms
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.

def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    else:
        raise Http404

def login_GET(request):
    login_form =  forms.loginForm()
    return render(request,'login_form.html',{'form':login_form})

def login_POST(request):
    login_form = forms.loginForm(request.POST)
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if login_form.is_valid and user is not None and user.is_active:   
        auth.login(request,user)
        #should make a profile manager and send user to his 
        #profile from here       
        return HttpResponse('you are login now ')
    else:
        return render(request,'login_form.html',{'form': login_form , 'errors':True})


def logout_GET(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect('/accounts/logout')
    else:
        return HttpResponse('you should login or register first')

def register_GET(request):
    registerForm = forms.registerForm()
    return render(request,'register.html',{'form':registerForm})

def register_POST(request):
    errors = []
    registerForm = forms.registerForm(request.POST)
    username = request.POST.get('username','')
    password1 = request.POST.get('password','')
    password2 = request.POST.get('re_password','')
    email = request.POST.get('email','')
    
    username_check = User.objects.filter(username = username)
    email_check = User.objects.filter(email = email)
    
    flag = True
    
    if not registerForm.is_valid:
        errors.extend(registerForm.errors)
        flag = False
    if not password1 == password2:
        errors.append('passwords dont mach together')
        flag = False
    if username_check.exists():
        print('username is exist')
        errors.append('this user name is exist')
        flag = False
    if email_check.exists():
        print('email is exist')
        errors.append('this email address is exist')
        flag = False

    if flag:

        print ('i am here')
        print('views line:58 inside if')     
        user = User.objects.create_user(
        username= username , email = email,password=password1
        )
        user.save()
        return login_POST(request)
   
    
    return render(request,'register.html',
    {'form': registerForm,'errors':errors})
