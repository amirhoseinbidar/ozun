# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site 
from users.utils.checks import check_user_is_own 
from users.models import  Profile  
from django.views.generic import CreateView ,DetailView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.http import Http404 
from django.contrib.auth.mixins import LoginRequiredMixin
from quizzes.form import examStartForm
 
class ProfileView(LoginRequiredMixin,DetailView):
    model =  Profile
    template_name = 'users/profile_view.html'

    def get(self,*args,**kwargs):
        if not get_user_model().objects.filter(pk = self.request.user.pk).exists():
            return Http404
         
        return super().get(*args,**kwargs)
    
    def get_object(self):  
        if not get_user_model().objects.filter(pk = self.request.user.pk).exists():
            return Http404
        
        if self.request.user.is_authenticated and not 'pk' in self.kwargs:            
            return self.model.objects.filter(user = self.request.user)
        
        try:    
            return self.model.objects.filter(user = self.kwargs['pk'])
        
        except KeyError:
            raise Http404

    def get_context_data(self,*args,**kwargs):
        data = super().get_context_data()
        profile  = self.get_object()[0]
        data['age_year'] , data['age_month'] = profile.get_user_age()
        data['domin'] = get_current_site(self.request).domain,
        data['form'] = examStartForm()
        print(examStartForm())
        if check_user_is_own(self.request , to =  profile.user.pk ):
            data['token']= get_random_string(length=30) 
            data['is_user_own'] =  True           
        else:
            data['is_user_own'] = False
        return data

# pofile updating perform by jquery and ajax because of
# some Tree like fields (interest_lesson , location , grade)
# they send data to rest API of this site for update profile
class ProfileEdit(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'users/profile_edit.html'

    def get_object(self):
        return self.model.objects.filter(user = self.request.user)

    def get(self,*args,**kwargs):
        is_exist = get_user_model().objects.filter(pk = self.request.user.pk).exists()
        is_own = check_user_is_own(self.request , to =  self.get_object()[0].user.pk) 
        
        if not is_exist  or not is_own:
            return Http404
        
        return super().get(*args,**kwargs)

    
