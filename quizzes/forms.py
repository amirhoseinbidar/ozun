# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from generics.forms import find_datas

#class quiz_answers_form(forms.Form):
#    def __init__(self, answer_list, ID , *args ,**kwargs):
#        super(self.__class__, self).__init__(*args,**kwargs)
#        self.fields['answer_{0}'.format(ID)] = forms.ChoiceField(
#            widget=forms.RadioSelect, choices=answer_list,label='')


#TODO Change in Lesson tree make this class useless
class quiz_select_form(forms.Form):#TODO:use of value_list instead of find_datas 
    pass
    #models = [
    #    Grade.objects.all(),
    #    Lesson.objects.all(),
    #]
    #firstBlankModels =  [
    #    Chapter.objects.all(),
    #    Topic.objects.all(),
    #    Source.objects.all(),
    #]
    #datafistBlank = find_datas(firstBlankModels, 'name', True)
    #data = find_datas(models,'name',False)
#
    #grade = forms.ChoiceField(
    #    widget=forms.Select, choices=data[0], label='grade')
    #lesson = forms.ChoiceField(
    #    widget=forms.Select, choices=data[1], label='lesson')
    #chapter = forms.TypedMultipleChoiceField(
    #    choices=datafistBlank[0], label='chapter', required=False)
#
    #topic = forms.MultipleChoiceField(
    #    widget=forms.SelectMultiple,
    #    choices=datafistBlank[1],
    #    label='topic',
    #    required=False)
#
    #source = forms.MultipleChoiceField(
    #    widget=forms.SelectMultiple,
    #    choices= datafistBlank[2],
    #    label='source',
    #    required=False)
#
    #level = forms.ChoiceField(
    #    widget=forms.Select, choices= (('-1','------'),)+levels_choice , label='level', required=False)
    #token = forms.CharField(widget = forms.HiddenInput )