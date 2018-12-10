# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model


class EmailAuthTests(TestCase) : #I dont know how to make a request manualy
    
    """ Test authenticate user's email address """ 
    
    def setUp(self):
        self.user = get_user_model().objects.create(username= 'some_user')
        

    def test_send_auth_email(self):
        response = self.client.get()
        
    
    def test_activate(self):
        response = self.client.get('/accounts/activate/{}/{}'.format(self.uidb,self.token))