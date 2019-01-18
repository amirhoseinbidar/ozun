# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from restAPI.serializers import UserSerializer , User , Profile , ProfileSerializer , ProfileUserSerializer
from users.utils.emailAuth import sendAuthEmail
from rest_framework.parsers import FileUploadParser


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    def post(self,request):
        response = super(UserCreate,self).post(request)
        
        username = request.data.get('username')
        email = request.data.get('email')
        
        user = User.objects.get(username = username)
        user.is_active  = False
        user.save()
        
        sendAuthEmail(request,user,email)
        response.data['notification'] = "a Authonticate email send to %s please open email and click on link for complete progress" %(email)
        
        return response

class ProfileView(generics.ListAPIView):
    serializer_class= ProfileSerializer
    
    def get_queryset(self):
        return Profile.objects.filter(pk = self.kwargs['pk'])
    
    def get(self,request,*args,**kwargs):
        response = super(ProfileView,self).get(request,*args,**kwargs)
        return self.response_maker(response)

    def response_maker(self,response):
        data = response.data
        if isinstance(data,list):
            data = data[0]
        user_data = list(User.objects.filter(pk = self.request.user.pk).values())[0]   
        user_data.pop('password',None)
        
        data.update( user_data )
        return response

class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'

class ProfileUpdate(ProfileView, generics.mixins.UpdateModelMixin,generics.GenericAPIView  ):
    parser_class = (ImageUploadParser,)
    serializer_class= ProfileSerializer
    def get_queryset(self):
        return Profile.objects.filter(user = self.request.user)
    
    def get_object(self):
        return Profile.objects.get(user = self.request.user)
        
    def update_user(self):
        data = {} 
        if 'last_name' in self.request.data:#TODO:Hard_Code 
            data['last_name'] = self.request.data.pop('last_name')
            if isinstance(data['last_name'],list):
                data['last_name'] = data['last_name'][0]
        if 'first_name' in self.request.data:
            data['first_name'] = self.request.data.pop('first_name')
            if isinstance(data['first_name'],list):
                data['first_name'] = data['first_name'][0]
        serializer = ProfileUserSerializer(self.request.user,data = data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def put(self,request,format =None,*args,**kwargs):
        isMutable = getattr(self.request.data,'_mutable' , None)
        
        if isMutable:
            self.request.data._mutable = True
        
        self.request.data['user'] = self.request.user.pk
        self.update_user() 
        
        if isMutable:
            self.request.data._mutable = False
        
        response = self.update(self.request,pk = self.request.user.pk,format = format,*args,**kwargs)
        
        return self.response_maker(response)
        