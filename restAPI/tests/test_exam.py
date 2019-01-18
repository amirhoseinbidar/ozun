# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import BaseAPITest
from django.urls import reverse
from quizzes.tests.test_embed import embed_test_quizzes
from quizzes.models import Exam
from json import dumps , loads

class ExamTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        embed_test_quizzes()
        self.client.login(username= 'test',password= 'test')
        self.exam_response = self.start_an_exam()
    
    def start_an_exam(self):
        url = reverse('api:start_exam',kwargs={'LessonPath':'دهم' })
        params = {
            'level' : 'hard',
            'source' : 'نشر الگو',
            'number' : '2',
        }
        return self.client.get(url,params)
    
    def test_start_exam(self):
        response = self.exam_response    
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        print(len(response.data[0]['quizstatus_set']))
        self.assertEqual(len(response.data[0]['quizstatus_set']), 2 , 
            'optional argument "number" did not work' )
        
    def test_update_exam(self):
        url = reverse('api:update_exam')
        quizzesStatus = Exam.objects.get(user = self.user).quizstatus_set.all()
        params = { 'quizstatus_set':[] }
        for status in quizzesStatus:
            params['quizstatus_set'].append(
                {
                    'quiz':status.quiz.pk,
                    'user_answer': status.quiz.answer_set.all()[0].pk,
                }
            )
        params = dumps(params)

        response = self.client.put(url,params,content_type = 'application/json')
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        

    def test_finish_exam(self):
        url = reverse('api:finish_exam')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        self.assertEqual(Exam.objects.get(user = self.user).is_active ,  False ,
            "some thing went wrong the exam didn't close ")
    
    def test_exam_info(self):
        url = reverse('api:exam_info' , kwargs={'exam_id':'active'})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        