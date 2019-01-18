# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.sites.shortcuts import get_current_site
from users.utils.checks import check_user_exists_decorator ,check_user_is_own
from users.utils.forms import signUpForm 
from users.models import  Profile  
from quizzes.forms import quiz_select_form
from .utils.emailAuth import sendAuthEmail
from django.views.generic import CreateView ,DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.http import Http404 

class SignUp(CreateView):
    model = get_user_model()
    template_name = 'users/signup.html'
    form_class = signUpForm
    
    def post(self,*args,**kwargs):
        response = super().post(*args,**kwargs)
        
        form = self.form_class(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sendAuthEmail(request,user,form.cleaned_data.get('email'))
        
        return response
    
    def get_success_url(self):
        return reverse('user:sign_up_secc')

#TODO: I sould chancge check_user_exist_decorator style

class ProfileView(DetailView):
    model =  Profile

    @check_user_exists_decorator
    def get(self,*args,**kwargs):
        super().get(*args,**kwargs)
    
    @check_user_exists_decorator
    def get_object(self):    
        if self.request.user.is_authenticated() and not 'pk' in self.kwargs:
            return self.model.objects.filter(user = self.request.user)
        
        try:    
            return self.model.objects.filter(user = self.kwargs['pk'])
        
        except KeyError:
            raise Http404


    def get_context_data(self,*args,**kwargs):
        data = super().get_context_data()
        data['age_year'] , data['age_month'] = self.object.get_user_age()
        data['domin'] = get_current_site(self.request).domain,
        
        if check_user_is_own(self.request , 'pk' , self.kwargs['pk'] ):
            data['quiz_select_form']= quiz_select_form( 
                    {'token' : get_random_string(length=30)} )
            data['is_user_own'] =  True           
        
        else:
            data['is_user_own'] = False
        
        return data

# pofile updating perform by jquery and ajax because of
# some Tree like fields (interest_lesson , location , grade)
# they send data to rest API of this site for update profile
class ProfileEdit(DetailView):
    model = Profile
    
    @check_user_exists_decorator
    def get(self,*args,**kwargs):
        super().get(*args,**kwargs)
    
