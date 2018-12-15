# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase , APIRequestFactory ,APIClient
from users.utils.emailAuth import sendAuthEmail , activate_user
from users.models import Profile
from django.urls import reverse
import json

class BaseAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.view = None

    @staticmethod
    def setup_user():
        return get_user_model().objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )
    
    @staticmethod
    def write_info(expect_code,recive_code):
        return 'Expected Response Code {}, received {} instead.'.format(
            expect_code,recive_code)


class UserCreateTest(BaseAPITest):
    def setUp(self):
        super(UserCreateTest,self).setUp()
    


    def test_create(self):
        url = reverse('api:create_user')
        params ={
            'username': 'test2',
            'password': '1234',
            'email': 'testuser2@test.com',
        }
        response = self.client.post(url,params)
        self.assertEqual(response.status_code,201,
            self.write_info(201,response.status_code) )
    
    def test_login(self):
        url = reverse('api:login')
        params = {
            'username':'test',
            'password':'test',
        }
        response = self.client.post(url,params)
        self.assertEqual(response.status_code,200,
            self.write_info(200,response.status_code) )


class UserProfileTest(BaseAPITest):
    def setUp(self):
        super(UserProfileTest,self).setUp()
        self.profile = activate_user(self.client,self.user)
          
    def test_update_profile(self):
        url = reverse('api:profile_update')
        self.client.login(username = 'test',password = 'test')
        params ={
            'first_name' : 'tester',
            'last_name': 'test man',
            # 'set_location'  :'تبریز/اسکو' ,   I will add this future
            'bio'  : 'for a tester every thing is a test',
            #'image' : '',   i dont know how can test it 
            'brith_day' : '2001-01-01',
            #'set_grade' : 'یازدهم ریاضی',
            #'set_interest_lesson' : 'یازدهم ریاضی/حسابان' ,
        }
        params = json.dumps(params)
        
        response = self.client.put(url,params,content_type='application/json')
        print(response.data,response.status_text)
        self.assertEqual(response.status_code,200,self.write_info(200,response.status_code) )

