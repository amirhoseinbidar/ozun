# -*- coding: utf-8 -*-
from __future__ import unicode_literals
        
from treebeard.mp_tree import MP_Node 
from core.checks import checkDuplicate 
from django.core.exceptions import ObjectDoesNotExist , ValidationError 
from core.exceptions import duplicationException , overDepthException
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

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

    name = models.CharField(max_length = 100,blank = False , null = False) 
    slug = models.CharField(max_length = 100,blank = True )
    type = models.CharField(choices = CONTENT_TYPE , max_length = 1,blank = False,null = False)

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
        checkDuplicate(TreeContent , self , name = self.name , type = self.type )
        
        if not self.slug:
            self.slug = slugify("{}".format(self.name) , True)

        if isinstance(self.type , int):
           self.type = TreeContent.getTypeByNumber(self.type)

        return super(TreeContent,self).save(*args,**kwargs)

    def __str__(self):
        types = dict(self.CONTENT_TYPE)
        try:
            return 'name : {} , type:  {}'.format(self.name , types[self.type])
        except:
            return 'name : {} , type:  {}'.format(self.name,self.type)


class LessonTree(MP_Node):
    content = models.ForeignKey(TreeContent,on_delete=models.CASCADE) 
        
    node_order_by = ['content']
    
    def add_root(self,*args,**kwargs):#it should be staticmethod but i dont know how call super method from staticmethod
        
        kwargs = self.treeContent_auto_create(**kwargs)
        newroot = kwargs.get('content',None)
        newroot = super(LessonTree,self).add_root(*args,**kwargs)
        
        try:
            newroot.check_Duplicate()
            newroot.check_depth(newroot)     
        except (duplicationException , overDepthException) as e  :
            newroot.delete()
            raise e
        
        return newroot

    def add_sibling(self,*args,**kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        newsibling = kwargs.get('content',None)    
        
        self.check_Duplicate(self,newsibling) 
        self.check_depth(self,newsibling) 
        
        return super(LessonTree ,self).add_sibling(*args,**kwargs)

    def add_child(self,*args,**kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        newchild = kwargs.get('content',None)
       
        self.check_Duplicate(self , newchild , func = 'get_children')
        self.check_depth(self ,  by=newchild , cheack_as_child= True)    
        
       
        return super(LessonTree ,self).add_child(*args,**kwargs)


    def move(self, *args,**kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        pos = kwargs.get('pos',None) or args[1]
        target =  kwargs.get('target',None) or args[0]
        
        if not pos or pos == 'sorted-sibling' : #diffualt is sorted-sibling
            self.check_Duplicate(target ,self)
            self.check_depth(target.get_parent(),self , cheack_as_child= True)

        elif pos == 'sorted-child' :
            self.check_Duplicate(target , self , 'get_children')# is target have any child  same with self
            self.check_depth(target,self,cheack_as_child=True)# can self  be child of target
        
        return super(LessonTree ,self).move(*args,**kwargs)

    def check_depth(self,object=None,by=None , cheack_as_child = False):
        if not object:
            object = self 
        
        if isinstance(object , LessonTree):
            objType = object.content.type 
        else:
            objType = object.type
        
        if by:
            if isinstance(by ,LessonTree):
                byType = by.content.type
            else:
                byType = by.type
        
        getNumber = TreeContent.getNumberByType

        if getattr(object,'depth',1) >= 5 and getattr(by,'depth',1) >= 5 :   
            raise overDepthException('can not make a root higher level then TOPIC')
        
        if not by :
            if getNumber(objType) != object.depth:
                raise overDepthException('content is in unallowed depth')
            return
        
        if  ( (not cheack_as_child and getNumber(objType) != getNumber(byType) ) or
              (cheack_as_child and (getNumber(objType)+1) != getNumber(byType) ) ):
            raise overDepthException('cant add this content to this depth')


    def check_Duplicate(self,object=None , by= None,func = 'get_siblings'):
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
            raise duplicationException('cant add a instance as child to a branch more then once')


    @staticmethod
    def find_by_path(path_str = None , get_by_slug = False):
        """ Find a lesson by its path """
        paths = path_str.split('/')
        object = LessonTree.get_root_nodes()
        index = 0
        for name in paths:
            if index == len(paths)-1:
                if get_by_slug:
                    object = object.get(content__slug = name)
                else :
                    object = object.get(content__name = name)
                break
            if get_by_slug:
                object = object.get(content__slug = name).get_children()
            else :
                object = object.get(content__name = name).get_children()
            index += 1
        return object
    
    @property
    def full_path(self):
        """ Turn a lesson location to a path """
        path_str = ''
        parent = self.get_parent()
        try:
            path_str += parent.full_path
        except AttributeError:
            return self.content.name

        path_str += '/'+self.content.name
        return path_str
    
    @staticmethod
    def create_by_path(path_str):
        """create objects in path if some of the 
            objects exist this method ignore them """
        paths = path_str.split('/')
        index =0
        lessonState = None
        for index in range(len(paths)):
            try:
                # go on tile you reach to a object that is not exist in path
                LessonTree.find_by_path('/'.join(paths[:(index+1)]))
            except ObjectDoesNotExist:
                # if object is not exist add it as previes object children
                _type = TreeContent.getTypeByNumber((index+1))
                
                if index == 0:
                    LessonTree().add_root(content_name = paths[index] , content_type = _type)
                    continue

                lessonState = LessonTree.find_by_path('/'.join(paths[:index]))
                lessonState.add_child(content_name = paths[index] , 
                    content_type = TreeContent.getTypeByNumber((index+1)))
        
        return lessonState

    def treeContent_auto_create(self,**kwargs):
        '''for creating content automaticly'''
        if 'content' in kwargs:
            return kwargs
        
        elif 'content_name' in kwargs and 'content_type' in kwargs:
            name = kwargs.pop('content_name')
            _type = kwargs.pop('content_type')
            try:
                content = TreeContent.objects.create(name = name,type = _type)
            except duplicationException:
                content = TreeContent.objects.get(name = name,type = _type)
            kwargs['content'] = content
        
        return kwargs


    def __str__(self):
        return u'%s' %(self.content)

def allowed_types(_type , field ,field_name):
    ''' check and if a uncorrect type have added will raise a error 
        use it in save method when you want to limit your types '''
    if not isinstance(_type , (list,tuple)):
        _type = [_type,]
    
    if field and not field.content.type in _type :
        types = dict(TreeContent.CONTENT_TYPE)
        error_text = 'unallowed type of content for field %s allowed types are %s' %(field_name , types)    
        raise ValidationError(error_text)
        
       
        

LESSON = TreeContent.LESSON
GRADE = TreeContent.GRADE
CHAPTER = TreeContent.CHAPTER
TOPIC = TreeContent.TOPIC