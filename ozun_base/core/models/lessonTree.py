# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from treebeard.mp_tree import MP_Node 
from core.checks import checkDuplicate
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from core.exceptions import duplicationException, overDepthException
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify


class TreeContent(models.Model):
    GRADE = 'G'
    LESSON = 'L'
    CHAPTER = 'C'
    TOPIC = 'T'
    CONTENT_TYPE = (
        (GRADE, 'grade'),
        (LESSON, 'lesson'),
        (CHAPTER, 'chapter'),
        (TOPIC, 'topic')
    )
    LAST_DEPTH = 4

    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.CharField(max_length=100, blank=True)
    type = models.CharField(choices=CONTENT_TYPE,
                            max_length=1, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    quote = models.CharField(max_length=255, blank=True)

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
        elif Type == TreeContent.LESSON:
            return 2
        elif Type == TreeContent.CHAPTER:
            return 3
        elif Type == TreeContent.TOPIC:
            return 4

        raise ValidationError('uncorrect type')

    def save(self, *args, **kwargs):
        checkDuplicate(TreeContent, self, name=self.name, type=self.type)

        if not self.slug:
            self.slug = slugify(self.name, True)

        if isinstance(self.type, int):
            self.type = TreeContent.getTypeByNumber(self.type)

        return super(TreeContent, self).save(*args, **kwargs)

    def __str__(self):
        types = dict(self.CONTENT_TYPE)
        try:
            return 'name : {} , type:  {}'.format(self.name, types[self.type])
        except:
            return 'name : {} , type:  {}'.format(self.name, self.type)


class LessonTree(MP_Node):
    content = models.ForeignKey(TreeContent, on_delete=models.CASCADE)

    node_order_by = ['content']

    @classmethod
    def add_root(cls, *args, **kwargs):
        kwargs = cls.treeContent_auto_create(cls, **kwargs)
        newroot = kwargs.get('content', None)
        newroot = super(LessonTree, cls).add_root(*args, **kwargs)
        return newroot

    def add_sibling(self, *args, **kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        return super().add_sibling(*args, **kwargs)

    def add_child(self, *args, **kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        return super().add_child(*args, **kwargs)

    def move(self, *args, **kwargs):
        kwargs = self.treeContent_auto_create(**kwargs)
        return super().move(*args, **kwargs)

    @staticmethod
    def find_by_path(path_str=None , get_by_slug = True):
        """ Find a lesson by its path """
        if not get_by_slug:
            path_str = slugify(path_str,True )
            
        paths = path_str.split('/')
        object = LessonTree.get_root_nodes()
        index = 0
        for name in paths:
            if index == len(paths)-1:
                object = object.get(content__slug=name)
                break
            object = object.get(content__slug=name).get_children()
            index += 1
        return object

    @property
    def full_path(self):
        """ Turn a lesson location to a path (use name)"""
        path_str = ''
        parent = self.get_parent()
        try:
            path_str += parent.full_path
        except AttributeError:
            return self.content.name

        path_str += '/'+self.content.name
        return path_str

    @property
    def full_path_slug(self):
        """ Turn a lesson location to a path (use slug) """
        path_str = ''
        parent = self.get_parent()
        try:
            path_str += parent.full_path_slug
        except AttributeError:
            return self.content.slug

        path_str += '/'+self.content.slug
        return path_str

    @staticmethod
    def create_by_path(path_str):
        """create objects in path if some of the 
            objects exist this method ignore them """
        paths = path_str.split('/')
        if len(paths) > TreeContent.LAST_DEPTH:
            raise ValidationError('Unallowed Depth , Last Depth is {}'.format(TreeContent.LAST_DEPTH) )

        index = 0
        lessonState = None
        for index in range(len(paths)):
            try:
                # go on tile you reach to a object that is not exist in path
                
                LessonTree.find_by_path('/'.join(paths[:(index+1)]), False)
            except ObjectDoesNotExist:
                # if object is not exist add it as previes object children
                _type = TreeContent.getTypeByNumber((index+1))

                if index == 0:
                    LessonTree().add_root(
                        content_name=paths[index], content_type=_type)
                    continue

                lessonState = LessonTree.find_by_path(
                    '/'.join(paths[:index]), False)
                lessonState.add_child(content_name=paths[index],
                                      content_type=TreeContent.getTypeByNumber((index+1)))

        return lessonState

    def treeContent_auto_create(self, **kwargs):
        '''for creating content automaticly'''
        if 'content' in kwargs:
            return kwargs

        elif 'content_name' in kwargs and 'content_type' in kwargs:
            name = kwargs.pop('content_name')
            _type = kwargs.pop('content_type')
            try:
                content = TreeContent.objects.create(name=name, type=_type)
            except duplicationException:
                content = TreeContent.objects.get(name=name, type=_type)
            kwargs['content'] = content

        return kwargs

    def __str__(self):
        return u'%s' % (self.content)


def allowed_types(_type, field, field_name):
    ''' check and if a uncorrect type have added will raise a error 
        use it in clean method when you want to limit your types '''
    if not isinstance(_type, (list, tuple)):
        _type = [_type, ]

    if field and not field.content.type in _type:
        error_text = 'unallowed depth of content for field %s allowed depth are %s' % (
            field_name, _type)
        raise ValidationError(error_text)


LESSON = TreeContent.LESSON
GRADE = TreeContent.GRADE
CHAPTER = TreeContent.CHAPTER
TOPIC = TreeContent.TOPIC
