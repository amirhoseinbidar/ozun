# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from core.models.lessonTree import LessonTree ,TreeContent , GRADE ,LESSON ,TOPIC,CHAPTER
from core.exceptions import duplicationException , ValidationError , overDepthException

class TreeContentTest(TestCase):

    def test_dublicate(self):
        
        grade = TreeContent(name = 'grade_test',type=GRADE)
        grade.save()
 
        grade2 = TreeContent(name = 'grade_test',type=GRADE)
        self.assertRaises(ValidationError,grade2.save)        
       


### LESSON TREE RULES: 
###     1. must not be sibligs with same name 
###     2. node depth and its level must be same 
###     3. can not add sub-branch to topics 
###
class LessonTreeTest(TestCase):
    
    def setUp(self):
        self.grade = LessonTree().add_root(
            content_name='grade_test',content_type = GRADE)
        self.lesson = self.grade.add_child(
            content_name='lesson_test',content_type = LESSON)
        self.chapter = self.lesson.add_child(
            content_name='chapter_test',content_type = CHAPTER)
        self.topic = self.chapter.add_child(
            content_name='topic_test',content_type = TOPIC)
   
    def test_auto_create_content(self):
        grade = self.grade.add_sibling(content_name = 'grade_test_2' 
            ,content_type = GRADE)
        
        self.assertEqual(grade.content.name , 'grade_test_2')
        self.assertEqual(grade.content.type , GRADE)

    def test_add_root(self):
        self.assertRaises(duplicationException, LessonTree().add_root 
            ,content_name = 'grade_test',content_type = GRADE) #RULE 1
        
        self.assertRaises(overDepthException , LessonTree().add_root
            , content_name='Lesson',content_type = LESSON) # RULE 2

    
    def test_add_child(self):
        self.assertRaises(duplicationException , self.chapter.add_child 
            , content_name='topic_test',content_type = TOPIC) # RULE 1

        self.assertRaises(overDepthException , self.chapter.add_child
            , content_name='chapter',content_type = CHAPTER) # RULE 2

        self.assertRaises(overDepthException , self.topic.add_child
            , content_name='something_test',content_type = TOPIC) #RULE 3
    
    def test_add_sibling(self):
        self.assertRaises(duplicationException , self.chapter.add_sibling
            , content_name='chapter_test',content_type = CHAPTER) #RULE 1

        self.assertRaises(overDepthException , self.lesson.add_sibling
            , content_name='chapter',content_type = CHAPTER) # RULE 2


    def test_move(self):
        grade2 = LessonTree().add_root(content_name = 'grade2' 
            , content_type = GRADE)
        lesson = grade2.add_child(content_name = 'lesson_test' 
            , content_type=LESSON )

        self.assertRaises(overDepthException, 
            self.topic.move , grade2,'sorted-sibling' ) # RULE 2
        self.assertRaises(overDepthException, 
            self.topic.move , grade2,'sorted-child' ) #RULE 2
        self.assertRaises(overDepthException, 
            grade2.move,target = self.topic,pos = 'sorted-child') #RULE 3
        self.assertRaises(duplicationException , self.lesson.move,
            lesson , pos = 'sorted-sibling' )  #RULE 1 
        self.assertRaises(duplicationException , self.lesson.move,
            grade2 , pos = 'sorted-child') #RULE 1