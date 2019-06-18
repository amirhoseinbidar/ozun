# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase , APIRequestFactory ,APIClient
from users.utils.emailAuth import sendAuthEmail 
from users.models import Profile
from django.urls import reverse
from quizzes.tests.test_embed import embed_test_quizzes
from quizzes.models import Quiz
from core.tests.test_embed import embed_test_locations , get_test_image_path
import json
from PIL import Image         

class BaseAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = self.setup_test_user()
        self.view = None


    @staticmethod
    def setup_test_user():
        return BaseAPITest.setup_user(
            'test','test','test@test.com')
    
    @staticmethod        
    def setup_user(username , password , email):
        return get_user_model().objects.create_user(
            username = username,
            email=email,
            password=password
        )
    
    @staticmethod
    def write_info(expect_code,response):
        status_text = getattr(response,'status_text',None) 
        status_code = getattr(response,'status_code',None)
        data = getattr(response,'data',None) or getattr(response,'content',None) 
        return 'Expected Response Code {}, received {} instead. \n error message: {} \n erro data:{}'.format(
            expect_code,status_code ,status_text,data)


#class UserProfileTest(BaseAPITest):#TODO this test have problem
#    def setUp(self):
#        super(UserProfileTest,self).setUp()
#        self.profile = ' ' #activate_user(self.client,self.user)
#        user2 = BaseAPITest.setup_user('user2','user2','user2@user2.com')
#        self.profile2 = ' ' #activate_user(self.client,user2)
#
#    def test_view(self):
#        url = reverse('api:profile_update')
#        self.client.login(username = 'test',password = 'test')
#        response = self.client.get(url)
#        self.assertEqual(response.status_code,200
#            ,self.write_info(200,response))
#        
#        url = reverse('api:profile_view',kwargs={'pk':self.profile2.pk})
#        self.client.login(username = 'user2',password = 'user2')
#        response = self.client.get(url)
#        self.assertEqual(response.status_code,200
#            ,self.write_info(200,response))
#
#
#    def test_update(self):
#        embed_test_quizzes()
#        embed_test_locations()
#        url = reverse('api:profile_update')
#        self.client.login(username = 'test',password = 'test')
#        with open(get_test_image_path(),'w+b') as image:
#            a = Image.new('RGB',(1000,1000))
#            a.save(image,'JPEG')
#            image.seek(0)
#            params ={
#                'first_name' : 'tester',
#                'last_name': 'test man',
#                'set_location'  :'تهران/ورامین/ورامین' , 
#                'bio'  : 'for a tester every thing is a test',
#                'image' : image,    
#                'brith_day' : '2001-01-01',
#                'set_grade' : 'یازدهم ریاضی',
#                'set_interest_lesson' : 'یازدهم ریاضی/حسابان' ,
#            }
#
#            header = {
#                'Content-Disposition': 'attachment; filename=test_image.jpg'
#            }
#
#            
#            response = self.client.put(url,params,format='multipart', **header)
#            
#        self.assertEqual(response.status_code,200,self.write_info(200,response) )
#

class QuizFeedBackTest(BaseAPITest):
    def setUp(self):
        super(QuizFeedBackTest,self).setUp()
        embed_test_quizzes()
        self.quiz = Quiz.objects.all()[1]
        self.url = reverse('api:quiz_feed_back',kwargs={'quiz_pk':self.quiz.pk})
        
    def test_vote(self):
        self.client.login(username = 'test',password = 'test')
        vote_before = self.quiz.total_votes
        response = self.client.post(self.url,{'feedback_type' : 'up vote'})        
        self.assertEqual(response.status_code,200,self.write_info(200,response))

        self.quiz.count_votes()
        self.assertEqual(self.quiz.total_votes-vote_before,1 , 
            "somthing went wrong , vote didn't add ")

class quizzesSearchTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        embed_test_quizzes()
        self.client.login(username = 'test',password = 'test')
    
    def test_search(self):
        url = reverse('api:search_quiz',kwargs={'action':'lasts'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
    def test_limited_search(self):
        url = reverse('api:search_selected_quiz',kwargs={'action':'lasts' , 'from':'1' , 'to':'3'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
    def test_most_voted(self):
        url = reverse('api:search_quiz',kwargs={'action':'most-voteds'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
    def test_limited_most_voted(self):
        url = reverse('api:search_selected_quiz',kwargs={'action':'most-voteds' , 'from':'1' , 'to':'3'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
    def test_path(self):
        url = reverse('api:search_lesson_path',kwargs={'action':'path' , 'LessonPath': 'دهم/فیزیک'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))

class QuizManagerTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        embed_test_quizzes()
        self.client.login(username = 'test',password = 'test')
    
    def test_create_quiz(self):
        url = reverse('api:quiz_create')
        params = {
            "answer_set": [
                {"content": "1","is_correct_answer": False},
                {"content": "2" ,"is_correct_answer": False},
                {"content": "3","is_correct_answer": False},
                {"content": "4","is_correct_answer": True}
            ],
            "lesson": "دهم/فیزیک",
            "added_by" : str(self.user.pk),
            "source": "نشر الگو" ,
            "content": " this is a test with math symbols like this $ sqrt{x^2} = |x| $ yeah this test is good  ",
            "exponential_answer": " and this is a exponential answer this have things  like this ",
            "level": "H",
        }
        response = self.client.post(url ,params,format='json')
        self.assertEqual(response.status_code,201,self.write_info(201,response))
    
    def test_update_quiz(self):
        self.test_create_quiz()
        quiz = Quiz.objects.get(added_by = self.user)
        url = reverse('api:quiz_update' , kwargs={'pk':quiz.pk})
        params = {
            "answer_set": [
                {'id':str(quiz.answer_set.all()[0]) ,"content": "1 test 1 ","is_correct_answer": False},
                {"content": "2 test 2 " ,"is_correct_answer": False},
                {"content": "3 test 3 ","is_correct_answer": False},
                {"content": "4 test 4 ","is_correct_answer": True}
            ],
            "lesson": "دهم/ریاضی",
            "added_by" : str(self.user.pk),
            "source": "قلم چی" ,
            "content": " this is a test with math symbols like this $ sqrt{x^2} = |x| $ yeah this test is good  ",
            "exponential_answer": " and this is a exponential answer update answer",
            "level": "E",
        }
        response = self.client.put(url,params,format='json')
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        



class LessonPathViewTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        embed_test_quizzes()
        self.client.login(username = 'test',password = 'test' )
    
    def test_get_path(self):
        url = reverse('api:lesson_path_view', kwargs= {'LessonPath': "یازدهم-ریاضی"})

        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        
        url = reverse('api:lesson_path_view', kwargs = { 'LessonPath' : 'دهم/فیزیک' })
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))

    def test_get_root(self):
        url = reverse('api:lesson_path_view' , kwargs = { 'LessonPath' : 'root' })
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
