# -*- coding: utf-8 -*-
from __future__ import unicode_literals
        
from treebeard.mp_tree import MP_Node
from core.checks import checkDublicate 
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from django.db import models

class TreeContent(models.Model):
    GRADE = 'G'
    LESSON = 'L'
    CHAPTER = 'C'
    TOPIC = 'T'
    CONTENT_TYPE = (
        (GRADE , 'grade'),
        (LESSON,'lesson'),
        (CHAPTER , 'chapter' ),
        (TOPIC , 'topic')
    )
    
    name = models.CharField(max_length = 100) 
    type = models.CharField(choices = CONTENT_TYPE , max_length = 1)

    @staticmethod 
    def getTypeByNumber(number):
        if number == 1:
            return TreeContent.GRADE
        elif number == 2:
            return TreeContent.LESSON
        elif number == 3:
            return TreeContent.CHAPTER
        elif number == 4:
            return TreeContent.TOPIC
        
        raise ValidationError('number out of range')
    @staticmethod
    def getNumberByType(Type):
        if Type == TreeContent.GRADE:
            return 1
        elif  Type == TreeContent.LESSON:
            return 2
        elif Type == TreeContent.CHAPTER:
            return 3
        elif  type == TreeContent.TOPIC:
            return 4
        
        raise ValidationError('uncorrect type')

    def save(self,*args,**kwargs):
        checkDublicate(TreeContent , self , name = self.name , type = self.type )
        
        if isinstance(self.type , int):
           self.type = TreeContent.getTypeByNumber(self.type)

        return super(TreeContent,self).save(*args,**kwargs)

class LessonTree(MP_Node):
     
    content = models.ForeignKey(TreeContent) 
        
    node_order_by = [content]
   
   
    def save(self,**kwargs):

        if self.depth >= 5 :
            raise ValidationError('can not make a root higher level then TOPIC')
        if TreeContent.getNumberByType(self.content.type) != self.depth:
            raise ValidationError('cant add this content to this depth')
              
        return super(LessonTree ,self).save()

def allowed_types(_type , field):
    def wrapper(func):
        def _decorator(**kwargs):
            self = kwargs.get('self')

            if not isinstance(_type , (list,tuple)):
                _type = [_type,]
            
            if not getattr(self , field).content.type in _type :
                raise ValidationError('unallowed type of content')
        return func
    return wrapper
        

LESSON = TreeContent.LESSON
GRADE = TreeContent.GRADE
CHAPTER = TreeContent.CHAPTER
TOPIC = TreeContent.TOPIC