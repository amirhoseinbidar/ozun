# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from studylab.settings import BASE_DIR
from django.core.exceptions import ValidationError
import os
from django.dispatch import receiver
from django.db.models.signals  import m2m_changed 
from django.contrib.auth.models import User

class membershipException(ValidationError):
    def __init__(self ,*args , **kwargs):
        self.code = 'membershipException'
        super(membershipException,self).__init__(*args,**kwargs)
class duplicateException(ValidationError):
    def __init__(self,*args,**kwargs):
        self.code = 'duplicateException'
        super(duplicateException,self).__init__(*args,**kwargs)
class unequalityException(ValidationError):
    def __init__(self,*args,**kwargs):
        self.code = 'unequalityException'
        super(unequalityException,self).__init__(*args,**kwargs)


def checkDublicate(klass,_self,attr):
    q = klass.objects.filter(**{attr : getattr(_self,attr)})
    if q.exists() and _self.pk != q[0].pk :# should not a name duplicate
            raise duplicateException('this {} is alredy exist'.format(attr))



class Source(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = "sources"
    def __unicode__(self):
        return u'{0}'.format(self.name)


class Grade(models.Model): #I can use of inheritance and hirechery model it take less code but little confusing   
    name = models.CharField(max_length= 30)
    def save(self , *args,**kwargs):
        checkDublicate(self.__class__ , self, 'name')
        super(self.__class__, self).save(*args,**kwargs)
    class Meta:
        db_table = "grades"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Lesson(models.Model):
    grades = models.ManyToManyField(Grade)
    name = models.CharField(max_length = 100)
    #diffrent grade can have same lesson we use of m2m instead add it for every one 
    def save(self , *args,**kwargs):
        checkDublicate(self.__class__ , self, 'name')
        super(self.__class__, self).save(*args,**kwargs)

    class Meta:
        db_table = "lessons"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Chapter(models.Model):
    lesson = models.ForeignKey(Lesson)
    #diffrent grades can have same chapter 
    grades = models.ManyToManyField(Grade)
    name = models.CharField(max_length = 100)

    def save(self):
        checkDublicate(self.__class__ , self, 'name')
        return super(self.__class__, self).save()
    
    class Meta:
        db_table = "chapter"
    def __unicode__(self):
        return u'{0}'.format(self.name )





class Topic(models.Model):#TODO:from db lesson isnot a foreignKey correct it 
    lesson = models.ForeignKey(Lesson)
     
    chapter = models.ForeignKey(Chapter)#diffrent grades can have same chapter
    
    grades = models.ManyToManyField(Grade)
    name = models.CharField(max_length = 100)
    
    
    def save(self,*args,**kwargs):
        checkDublicate(self.__class__ , self, 'name')

        if self.chapter.lesson.pk != self.lesson.pk:
            raise unequalityException('Topic.lesson and chapter.lesson must be same')
        

        return super(self.__class__, self).save()
    
    class Meta:
        db_table = "topics"
    def __unicode__(self):
        return u'{0}'.format(self.name )



class Exponential_answer(models.Model):
    text = models.TextField(blank = True)
    image = models.ImageField(blank = True,null = True,upload_to='exponential_answers/images')
    video = models.FileField(blank = True,null = True,upload_to='exponential_answers/videos')
    extra = models.FileField(blank = True,null = True,upload_to='exponential_answers/extras')
    #mybe something else will add 
    def __unicode__(self):
        return u'{0}'.format(self.pk)

class Answers(models.Model):
    text = models.TextField()
    def __unicode__(self):
        return u'answer id: {0}'.format(self.pk)


levels_choice = (
    ('VH' , 'very hard'),
    ('H' , 'hard'),
    ('M' , 'medium'),
    ('E' , 'easy'),
    ('VE' , 'very easy'),
)

class Quizzes(models.Model):
    text = models.TextField() 
    #NOTE: actually answer have a many to one relation with a quiz but
    # for rule 1 we should control correct_answer and quiz_answer relation 
    # and admin site make problem when we will make a custom admin part will correct it 

    quiz_answers = models.ManyToManyField(Answers)#RULE 1:correct_answers should be one of the quiz_answers
    
    correct_answer = models.ForeignKey(Answers,related_name='correct_answer')
    image = models.ImageField(blank = True,null = True, upload_to = 'quizzes/images')
    exponential_answer= models.ForeignKey(to = Exponential_answer,blank= True,null = True )
    source = models.ForeignKey(Source)
    level = models.CharField(max_length = 5,choices =levels_choice )
    #every quiz must determine its lesson and grade  but topic is optional we can let it empty
    grade = models.ForeignKey(Grade) 
    lesson = models.ForeignKey(Lesson)#RULE 2:grade should be in the lesson.grade
    topics = models.ManyToManyField(Topic, blank = True)#RULE 3:topics must be members of lesson
    timeOut = models.DateTimeField(blank = True,null = True)
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)
        
    def isAnswerFieldValid(self):
        return self.quiz_answers.filter(pk = self.correct_answer.pk).exists() 

    def isTopicsFieldValid(self):
        return self.topics.filter(lesson__pk = self.lesson.pk).count() == self.topics.count()
        # is all of the topics from determined lesson  
    
    def save(self,*args,**kwargs):
        if not self.lesson.filter(grades__pk = self.grade.pk).exists():
            raise membershipException('grade should be member of lesson.grades')
        super(Quizzes,self).save(*args,**kwargs)

    def get_all_topics(self):#TODO : i should repair it
        data = {}
        data['grades'] = grade_list = []
        data['lessons'] = lesson_list = []
        data['chapters'] = chapter_list = []
        data['topics'] = topic_list = []
        for choice in self.topic:
            grade_list.append(choice.grade.name)
            lesson_list.append(choice.lesson.name)
            chapter_list.append(choice.chapter.name)
            topic_list.append(choice.name)
        return data
    class Meta:
        db_table = "quizzes"
    def __unicode__(self):
        return u'{0}'.format(self.pk)


@receiver(m2m_changed,sender = Topic.grades.through)
@receiver(m2m_changed,sender = Chapter.grades.through)
@receiver(m2m_changed,sender = Quizzes.topics.through)
@receiver(m2m_changed,sender = Quizzes.quiz_answers.through )
def Quizzes_m2m_control(**kwargs): # for perform RULE 1 and 3
    action = kwargs.pop('action', None)
    instance = kwargs.pop('instance' , None)
    sender = kwargs.pop('sender' , None)
    

    
    if (action == 'post_add' or action == 'post_remove'):#NOTE: in signal methods if you raise a exception all data back to previous 
        
        if sender is Quizzes.topics.through:
            if not instance.isTopicsFieldValid(): 
                raise membershipException('topics must be members of lesson')
        
        elif sender is Quizzes.quiz_answers.through:
            if not instance.isAnswerFieldValid():
                raise membershipException('correct_answers should be one of the quiz_answers')
        
        elif sender is Chapter.grades.through:
            lesson_grades = instance.lesson.grades.all()
            print lesson_grades
            if instance.grades.filter(pk__in = lesson_grades ).count() != instance.grades.all().count():
                raise membershipException(message = 'all of Chapter.grade must be members of Chapter.lesson.grade')
        
        elif sender is Topic.grades.through:
            chaptre_grades = instance.chapter.grades.all()
            if instance.grades.filter(pk__in = chaptre_grades ).count() != instance.grades.all().count():
                raise membershipException(message = 'all of Topic.grades must be members of Topic.chapter.grades')
       
        
    
   


class Quizzes_status(models.Model):#RULE: user_answer  must be one of the quiz answers or None
    quiz = models.ForeignKey(Quizzes)
    user_answer = models.ForeignKey(Answers,blank = True,null = True)
    
    def save(self,*args,**kwargs):
        
        flag = False
        
        if not self.user_answer:# if user_answer is Null pass it
            flag = True
        else:
            flag = self.quiz.quiz_answers.filter(pk = self.user_answer.pk).exists()            
        
        if flag:
            return super(self.__class__, self).save(*args,**kwargs)
    
        raise membershipException(message =  'user_answer should be one of the quiz.quiz_answers')
    class Meta:
        verbose_name_plural = 'Quizzes statuses'


    @staticmethod
    def saveFromQuizzesSet(quizzes):
        data = []
        print quizzes
        for quiz in quizzes:
            quiz_status = Quizzes_status(quiz = quiz,user_answer = None)
            quiz_status.save()
            data.append(quiz_status.pk)
        return Quizzes_status.objects.filter(pk__in = data)
    
    @staticmethod
    def saveFromDict(dictionary):#RULL dictionary is like this {quiz_status_pk:##,answer_pk:##} 
        quiz =  Quizzes_status.objects.get(pk = dictionary['quiz_status_pk'])
        quiz.user_answer = Answers.objects.get(pk = dictionary['answer_pk'])
        quiz.save()
        return quiz
    @staticmethod
    def saveFromDictList(data):
        List = []
        for dic in data:
            List.append(Quizzes_status.saveFromDict(dic).pk)
        return Quizzes_status.objects.filter(pk__in = List)

