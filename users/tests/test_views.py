# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_webtest import WebTest
from django.test import TestCase , Client
from django.urls import reverse
from users.models import Profile
from django.contrib.auth import get_user_model

class BaseUsersTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username= 'test' ,email = 'test@test.com')
        self.user.set_password('1234')
        self.profile  = Profile(user = self.user)
        self.profile.save()


class SignUpTest(WebTest): 
    
    def test_sign_up(self):
        page = self.app.get(reverse('users:sign_up'))
        page.form['user name'] = 'test'
        page.form['email'] = 'test@test.com'
        page.form['password'] = '!@#$qwER43'
        page.form['password 2'] = '!@#$qwER43'
        page = page.form.submit()
        self.assertRedirects(page, reverse('users:controller'))

class LoginTest(BaseUsersTest,WebTest):
    
    def test_login(self):
        page = self.app.get(reverse('user:login'))
        page.form['user name'] = 'test'
        page.form['password'] = '1234'
        page = page.form.submit()
        self.assertRedirects(page, self.profile.get_absolute_url())

class ProfileTest(BaseUsersTest):
    
    def test_view_for_owner(self):
        pass
    
    def test_view_for_others(self):
        pass    
    
    def test_edit_get(self):
        pass
    
    def test_edit_pst(self):
        pass
    

    
    