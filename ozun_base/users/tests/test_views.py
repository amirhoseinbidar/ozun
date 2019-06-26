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


class ProfileTest(BaseUsersTest):
    
    def test_view_for_owner(self):
        pass
    
    def test_view_for_others(self):
        pass    
    
    def test_edit_get(self):
        pass
    
    def test_edit_pst(self):
        pass
    

    
    