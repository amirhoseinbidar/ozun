# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics ,status , viewsets , mixins
from rest_framework.mixins import (
    CreateModelMixin ,
    DestroyModelMixin,
    ListModelMixin ,
    RetrieveModelMixin ,
    UpdateModelMixin
)
from rest_framework.response import Response
from qa.models import Question ,Answer 
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ParseError
from ..serializers.qa import QuestionSerializer ,AnswerSerializer
from users.models import User
from ..utils import IsOwnerMixin , WriteOnlyViewSetMixin


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        state = self.kwargs('state')

        if state == 'id':
            return Question.objects.filter(pk = self.kwargs['id'])
        elif state == 'title':
            return Question.objects.filter(slug = self.kwargs['title'])
        elif state == 'answered':
            return Question.objects.get_answered()
        elif state == 'unanswered':
            return Question.objects.get_unanswered()
        else:
            raise ParseError('Uncorrect Argoment')

class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    def get_queryset(self):
        return Answer.objects.filter(pk = self.kwargs['id']) 


class QuestionViewSet(IsOwnerMixin ,viewsets.ModelViewSet ):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(
    IsOwnerMixin ,
    WriteOnlyViewSetMixin):
        serializer_class = AnswerSerializer
        queryset = Answer.objects.all()


class QAHandler(generics.views.APIView):
    def post(self,request, _type):
        if _type == 'question':
            if not 'question' in self.request.data:
                raise ParseError('need a ""question"" attrebute wiche contain question id ')
            return self._vote_handler(Question,self.request.data['question'])
        
        if _type == 'answer':
            if not 'answer' in self.request.data:
                raise ParseError('need a ""answer"" attrebute wiche contain answer id ')
            return self._vote_handler(Answer, self.request.data['answer'])
        
        if _type == 'accept_answer':
            if not 'answer' in self.request.data:
                raise ParseError('need a ""answer"" attrebute wiche contain answer id ')
            return self._accept_answer()

    def _vote_handler(self,model , id):
        #answer and question vote handler is same
        """Function view to receive post call, returns the count of votes a given
            answer has recieved."""
        if not "feedback_type" in self.request.data:
            raise ParseError('please add a feedback_type')

        value = self.request.data["feedback_type"] 
        
        if value != "U" and value != 'D': #UPVOTE or DOWNVOTE
            raise ParseError('Uncorrect Feedback') 

        obj = model.objects.filter(pk=id)
        if not obj:
            raise ParseError('Question does not exist')
        
        obj = obj[0]
        
        try:
            obj.votes.update_or_create(
                user=self.request.user, defaults={"feedback_type": value}, )
            obj.count_votes()
            return JsonResponse({"votes": obj.total_votes})

        except IntegrityError:  # pragma: no cover
            return JsonResponse({'status': 'false',
                                 'message': _("Database integrity error.")},
                                status=500)

    def _accept_answer(self):
        """Function view to receive post call, marks as accepted a given answer for
        an also provided question."""
        answer_id = self.request.data["answer"]
        answer = Answer.objects.get(id=answer_id)
        answer.accept_answer()
        return JsonResponse({'status': 'OK'}, status=200)



