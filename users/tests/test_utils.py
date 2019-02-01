# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase ,RequestFactory
from django.contrib.auth import get_user_model
from users.utils.emailAuth import activate ,sendAuthEmail

class EmailAuthTests(TestCase) : #I dont know how to make a request manualy
    
    """ Test authenticate user's email address """ 
    
    def setUp(self):
        self.user = get_user_model().objects.create(
            username= 'some_user' ,email = 'some_email@test.com')
        self.user.set_password('1234')
        self.factory = RequestFactory()

    def test_send_auth_email(self):
        request = self.factory.get('/accounts/register/')
        mail_context = sendAuthEmail(request,self.user,self.user.email)
        
        self.assertIsNotNone(mail_context)
        self.assertNotEqual(mail_context['uid'],'')
        self.assertNotEqual(mail_context['token'],'')

        self.uid = mail_context['uid']
        self.token = mail_context['token']
        
        response = self.client.get('/accounts/activate/{}/{}/'.format(self.uid,self.token))
        self.assertEqual(response.status_code,302) 
        