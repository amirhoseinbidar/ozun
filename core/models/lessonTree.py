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
        elif  Type == TreeContent.TOPIC:
            return 4
        
        raise ValidationError('uncorrect type')

    def save(self,*args,**kwargs):
        checkDublicate(TreeContent , self , name = self.name , type = self.type )
        
        if isinstance(self.type , int):
           self.type = TreeContent.getTypeByNumber(self.type)

        return super(TreeContent,self).save(*args,**kwargs)

    def __str__(self):
        types = dict(self.CONTENT_TYPE)
        return u'name : %s , type:  %s' %(self.name , types[self.type])

class LessonTree(MP_Node):
    content = models.ForeignKey(TreeContent,on_delete=models.CASCADE) 
        
    node_order_by = ['content']
    
    def add_sibling(self,*args,**kwargs):
        newsibling = kwargs.get('content',None) 
        self.check_depth(self,newsibling)    
        self.check_dublicate(self,newsibling) 
        
        return super(LessonTree ,self).add_sibling(*args,**kwargs)

    def add_child(self,*args,**kwargs):
        newchild = kwargs.get('content',None)
        self.check_depth(self , newchild ,True )    
        self.check_dublicate(self , newchild , func = 'get_children')
       
        return super(LessonTree ,self).add_child(*args,**kwargs)


    def move(self, *args,**kwargs):
        pos = kwargs.get('pos',None)
        if pos == 'sorted-sibling':
            self.check_dublicate(args[0] ,self)
            self.check_depth(args[0].get_parent(),self , cheack_as_child= True)

        elif pos == 'sorted-child':
            self.check_dublicate(args[0] , self , 'get_children')# is in args[0] child any dublicate with self
            self.check_depth(args[0],self,cheack_as_child=True)# is self can be child of args[0]
        
        super(LessonTree ,self).move(*args,**kwargs)

    def check_depth(self,object=None,by=None , cheack_as_child = False):
        if not object:
            object = self 
        if isinstance(object , LessonTree):
            objType = object.content.type 
        else:
            objType = object.type
        if isinstance(by ,LessonTree):
            byType = by.content.type
        else:
            byType = by.type
        
        getNumber = TreeContent.getNumberByType

        if getattr(object,'depth',1) >= 5 and getattr(by,'depth',1) >= 5 :   
            raise ValidationError('can not make a root higher level then TOPIC')
        
        if not by :
            if getNumber(objType) != object.depth:
                raise ValidationError('content is in unallowed depth')
            return
        
        if  ( (not cheack_as_child and getNumber(objType) != getNumber(byType) ) or
              (cheack_as_child and (getNumber(objType)+1) != getNumber(byType) ) ):
            raise ValidationError('cant add this content to this depth')

    def check_dublicate(self,object=None , by= None,func = 'get_siblings'):
        if not object:
            object = self
        if not by:
            by = object
        
        if isinstance(by , TreeContent):
            check_buf =  getattr(object,func)().filter(content__name = by.name ,
                 content__type = by.type).exists()
        else :
            check_buf = getattr(object,func)().filter(
                    content = by.content).exclude(pk = by.pk).exists()
        if check_buf :
            raise ValidationError('cant add a instance as child to a branch more then once')

    @staticmethod
    def find_by_path(path_str):
        pathes = path_str.split('/')
        object = LessonTree.get_root_nodes()
        index = 0
        for name in pathes:
            if index == len(pathes)-1:
                object = object.get(content__name = name)
                break
            object = object.get(content__name = name).get_children()
            index += 1
        return object
    def turn_to_path(self):
        path_str = ''
        parent = self.get_parent()
        try:
            path_str += parent.turn_to_path()
        except AttributeError:
            return self.content.name

        path_str += '/'+self.content.name
        return path_str

#NOTE: I still dont need this function
#   def treeContent_auto_create(**kwargs):


    def __str__(self):
        return u'%s' %(self.content.name)

def allowed_types(_type , field ,field_name):
    if not isinstance(_type , (list,tuple)):
        _type = [_type,]
    
    if field and not field.content.type in _type :
        types = dict(TreeContent.CONTENT_TYPE)
        error_text = 'unallowed type of content for field %s allowed types are %s' %(field_name , types[_type])    
        raise ValidationError(error_text)
        
       
        

LESSON = TreeContent.LESSON
GRADE = TreeContent.GRADE
CHAPTER = TreeContent.CHAPTER
TOPIC = TreeContent.TOPIC