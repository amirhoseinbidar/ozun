# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from studylab.settings import BASE_DIR
from django.core.exceptions import ValidationError
import os
from django.dispatch import receiver
from django.db.models.signals  import m2m_changed , post_save , pre_save , pre_delete , post_delete
from studylab.generic import cache_list,Cache

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



class Source(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = "sources"
    def __unicode__(self):
        return u'{0}'.format(self.name)



class Grade(models.Model): #I can use of inheritance and hirechery model it take less code but little confusing   
    name = models.CharField(max_length= 30)
    def save(self):
        if self.__class__.objects.filter(name = self.name).exists():# should not a name duplicate
            raise duplicateException('this name is alredy exist')
        
    class Meta:
        db_table = "grades"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Lesson(Grade):
    grades = models.ManyToManyField(Grade) 
    #diffrent grade can have same lesson we use of m2m instead add it for every one 

    class Meta:
        db_table = "lessons"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Chapter(Lesson):
    lesson = models.ForeignKey(Lesson)
    #diffrent grades can have same chapter 
   
    def save(self):
        if self.grades.filter(pk__in = self.lesson.grades.value_list('pk') ).count()!= self.grades.all().count():
             raise membershipException(message = 'all of Chapter.grade must be members of Chapter.lesson.grade')

        return super(self.__class__, self).save()
    class Meta:
        db_table = "chapter"
    def __unicode__(self):
        return u'{0}'.format(self.name )

class Topic(Chapter):#TODO:from db lesson isnot a foreignKey correct it 
    chapter = models.ForeignKey(Chapter)
    
    def save(self,*args,**kwargs):
        if self.chapter.lesson.pk != self.lesson.pk:
            raise unequalityException('Topic.lesson and chapter.lesson must be same')

        if self.grades.filter(pk__in = self.chapter.grades.value_list('pk')).count() != self.grades.all().count():
            raise membershipException(message = 'all of Topic.grades must be members of Topic.chapter.grades')
       
        

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
    
        
    def isAnswerFieldValid(self):
        return self.quiz_answers.filter(pk = self.correct_answer.pk).exsist()

    def isTopicsFieldValid(self):
        return self.topics.filter(lesson__pk = self.lesson.pk).count() == self.topics.count()
        # is all of the topics from determined lesson 
          
            
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




@receiver(m2m_changed,sender = Quizzes.topics.through )
@receiver(m2m_changed,sender = Quizzes.quiz_answers.through )
def Quizzes_m2m_control(**kwargs): # for perform RULE 1 and 3
    action = kwargs.pop('action', None)
    instance = kwargs.pop('instance' , None)
    sender = kwargs.pop('sender' , None)
    
    
    if action == 'pre_add' or action == 'pre_remove':#cache previous data 
        cache = Cache()
        cache.quiz_answers = instance.quiz_answers.all()
        cache.topics = instance.topics.all()
        string = ''
        if sender is Quizzes.topics.through:
            string = 'topics'
        if sender is Quizzes.quiz_answers.through:
            string = 'quiz_answer'
        
        cache_list.add_record(string , instance.pk , cache)
   
    
    if (action == 'post_add' or action == 'post_remove') and (cache_list.find(id = instance.pk)):
        
        if sender is Quizzes.topics.through:
            if not instance.isTopicsFieldValid(): # if is not correct come back to previous data and raise exception
                instance.topics = cache_list.find(flag='topics',id= instance.pk).topics
                instance.save()
                raise membershipException('topics must be members of lesson')
        
        if sender is Quizzes.quiz_answers.through:
            if not instance.isAnswerFieldValid():
                instance.quiz_answers = cache_list.find(flag = 'quiz_answer',id = instance.pk).quiz_answers
                instance.save()
                raise membershipException('correct_answers should be one of the quiz_answers')
       
        cache_list.delete(id= instance.pk)
    
   


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

