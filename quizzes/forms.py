# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from general_views.forms import find_datas
from quizzes.models import Grade, Lesson, Chapter, Topic, Source, Level


class quiz_answers_form(forms.Form):
    def __init__(self, answer_list, ID , *args ,**kwargs):
        super(self.__class__, self).__init__(*args,**kwargs)
        self.fields['answer_{0}'.format(ID)] = forms.ChoiceField(
            widget=forms.RadioSelect, choices=answer_list,label='')
            #TODO: data must be unclean but it clean automaticlly i should turn off it  


class quiz_select_form(forms.Form):
    models = [
        Grade.objects.all(),
        Lesson.objects.all(),
        Chapter.objects.all(),
        Topic.objects.all(),
        Source.objects.all(),
        Level.objects.all(),
    ]
    data = find_datas(models, 'name', True)

    grade = forms.ChoiceField(
        widget=forms.Select, choices=data[0], label='grade')
    lesson = forms.ChoiceField(
        widget=forms.Select, choices=data[1], label='lesson')
    chapter = forms.TypedMultipleChoiceField(
        choices=data[2], label='chapter', required=False)

    topic = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=data[3],
        label='topic',
        required=False)

    source = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=data[4],
        label='source',
        required=False)

    level = forms.ChoiceField(
        widget=forms.Select, choices=data[5], label='level', required=False)
