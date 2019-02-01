# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from core.models import LessonTree
from quizzes.models import Quiz,Answer,Source
from core.tests.test_embed import create_documents

def embed_test_quizzes(): #TODO:this can be smaller
    documents = create_documents('quizzes.yaml')
    
    for data in documents:
        document = data.pop('document',None)
        
        if document == 'paths':
            for key in data:
                LessonTree.create_by_path(data[key])
        
        if document == 'quizzes':
            for key in data.keys():  
                dic = data[key]
                answers = dic.pop('answers',None)
                
                dic['source'] = Source(name = dic['source'])
                dic['source'] = dic['source'].save_or_get()

                dic['lesson'] = LessonTree.find_by_path(dic['lesson'])
                quiz = Quiz(**dic)
                quiz.save()
                answer_objects = []
                for answer in answers :
                    ans = Answer(quiz = quiz ,
                        is_correct_answer = answer['is_correct_answer'],
                        content = dic['content'] )
                    ans.save()
                    answer_objects.append(ans)

