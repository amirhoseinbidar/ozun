# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models
from django import forms
from quizzes.models import Quiz , Answer
from json import dumps , loads
from django.core.exceptions import ValidationError

class quizAdminRules(admin.ModelAdmin):
    
    def get_queryset(self, request):
        queryset = super(quizAdminRules ,self).get_queryset(request)
        if not request.user.is_superuser:
           queryset = queryset.filter(added_by = request.user)
        return queryset


    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super(quizAdminRules,self).save_model(request, obj, form, change)

class quizzesAdmin(quizAdminRules):
    
    readonly_fields = ['added_by']
    #def address(self,obj):
    #    base = '{}/{}'.format(obj.grade.name , obj.lesson.name)
    #    data = ''
    #    if not obj.topics.all().exists():
    #        return base
    #    for topic in obj.topics.all():
    #        data += base+'/{}/{} \n '.format(topic.chapter.name ,topic.name)
    #    
    #    return data

    #def answersJson(self , quiz):
    #    data = []
    #    for answer in quiz.answers_set.all():
    #        data.append( {
    #            'text': answer.text,
    #            'pk' : answer.pk
    #        })
    #        
    #    return dumps(data,ensure_ascii=False)
    
    
    def answersController(self,Dict,quiz):#TODO:the value of Dict should be safe this method dont check data is clear or not 
        for i in Dict:
            if isinstance(i,str) and i.find('answer-info') != -1 : #answer-info-$$ is hidden input that have information about a answer in json format see /static/scripts/quizzes/admin-change_form.js
                info = loads(Dict[i])
                txt = Dict[info['connect_to']]
                if not txt:
                    raise ValidationError('empety field error0')
                if info['is_new']:	
                    Answer(text=txt , quiz = quiz).save()
                else:
                    answer = Answer.objects.get(info['pk'])
                    answer.text = txt
                    answer.save()
					
    def change_view(self, request, object_id, form_url='', extra_context=None):
        
        extra_context = extra_context or {}
        #extra_context['answersJson'] = self.answersJson( Quiz.objects.get(id = object_id) )
        extra_context['is_quizzesAdmin']= True
        
        return super(quizzesAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    def save_model(self, request, obj, form, change):
        model = super(self.__class__,self).save_model(request,obj,form,change)
		
    list_display = ('level','timestamp')

class topicAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']
    
class chapterAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']
    
class lessonAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']
     
class QuizzesAdminSite(admin.AdminSite):
    site_header = "StudyLab Quizzes Admin"
    site_title = 'StudyLab Quizzes Admin Portal'
    index_title = 'Welome to Quizzes Administration Portal'

quizzesAdminSite = QuizzesAdminSite(name='quizzes_admin')

# Register your models here.
quizzesAdminSite.register(models.Quiz,quizzesAdmin)
quizzesAdminSite.register(models.Source)
quizzesAdminSite.register(models.Answer)
quizzesAdminSite.register(models.QuizStatus)

