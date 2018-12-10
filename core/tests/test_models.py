# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from core.models.lessonTree import LessonTree ,TreeContent , GRADE ,LESSON ,GRADE,CHAPTER
from core.exception import duplicateException , ValidationError

class TreeContentTest(TestCase):

    def test_dublicate(self):
        
        grade = TreeContent(name = 'grade_test',type='G')
        grade.save()

        is_failed = False
        try: 
            grade2 = TreeContent(name = 'grade_test',type='G')
            grade2.save()        
        except duplicateException :
            is_failed = True
        self.assertEqual(is_failed,True)

class LessonTreeTest(TestCase):
    def setUp(self):
        pass


    def test_auto_create_content(self):
        grade = LessonTree().add_root(content_name = 'grade_test' ,content_type = GRADE)
        
        self.assertEqual(grade.content.name , 'grade_test')
        self.assertEqual(grade.content.type , GRADE)

    def test_add_root(self):
        try:
            lesson = LessonTree().add_root(content_name = 'lesson_test',content_type = LESSON)
        except ValidationError : # if faild test is ok 
            return

        lesson.check_depth()
        lesson.check_dublicate()
    
    def test_add_child(self):
        pass
    def test_add_sibling(self):
        pass
    def test_move(self):
        pass

                

