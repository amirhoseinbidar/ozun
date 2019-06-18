# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics ,status
from rest_framework.response import Response
from qa.models import Question ,Answer 
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ParseError
from ..qa_serializer import QuestionSerializer ,AnswerSerializer
from users.models import User
from users.utils.checks import check_user_is_own

class LastQuestionsView(generics.ListAPIView):
    """CBV to render a list view with all the registered questions."""
    serializer_class = QuestionSerializer
    
    def get_queryset(self,**kwargs):
        return Question.objects.all()

    
    def get(self,*args,**kwargs): 
        response = super().get(*args,**kwargs)
        response.data.append( ("popular_tags", Question.objects.get_counted_tags()) )
        response.data.append( ("active" , "all") )
        return response

class QuestionAnsListView(generics.ListAPIView):
    """CBV to render a list view with all question which have been already
    marked as answered."""
    serializer_class = QuestionSerializer

    def get_queryset(self, **kwargs):
        return Question.objects.get_answered()

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        response.data.append( ("active" , "answered") )
        return  response

class QuestionListView(generics.ListAPIView):
    """CBV to render a list view with all question which have been already
    marked as answered."""
    serializer_class = QuestionSerializer

    def get_queryset(self, **kwargs):
        return Question.objects.get_unanswered()

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        response.data.append( ("active" , "unanswered") )
        return  response

class QuestionDetailView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    def get_queryset(self,**kwargs):
        return Question.objects.filter(pk = self.kwargs['pk'])
    
class CreateQuestionView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    def post(self,*args,**kwargs):
        if 'user' in self.request.data:
            user = User.objects.filter(pk = self.request.data['user'])
            if user.exists() and not check_user_is_own(self.request,user[0].pk):
                raise ParseError('you cant answer as another user')
        return super().post(*args,**kwargs)

class CreateAnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    def post(self,*args,**kwargs):
        if 'user' in self.request.data:
            user = User.objects.filter(pk = self.request.data['user'])
            if user.exists() and not check_user_is_own(self.request,user[0].pk):
                raise ParseError('you cant answer as another user')
        return super().post(*args,**kwargs)
        

class QAHandler(generics.views.APIView):
    def post(self,request, _type):
        if _type == 'question':
            if not 'question' in self.request.data:
                return ParseError('need a ""question"" attrebute wiche contain question id ')
            return self._vote_handler(Question,self.request.data['question'])
        
        if _type == 'answer':
            if not 'answer' in self.request.data:
                return ParseError('need a ""answer"" attrebute wiche contain answer id ')
            return self._vote_handler(Answer, self.request.data['answer'])
        
        if _type == 'accept_answer':
            if not 'answer' in self.request.data:
                return ParseError('need a ""answer"" attrebute wiche contain answer id ')
            return self._accept_answer()

    def _vote_handler(self,model , id):
        #answer and question vote handler is same
        """Function view to receive post call, returns the count of votes a given
            answer has recieved."""
        value = None
        
        if self.request.data["feedback_type"] == "U":
            value = 'U' #Up vote
        else:
            value = 'D' #Down vote

        obj = model.objects.get(pk=id)
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
        answer = Answer.objects.get(uuid_id=answer_id)
        answer.accept_answer()
        return JsonResponse({'status': 'true'}, status=200)



