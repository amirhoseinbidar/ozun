from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import ListModelMixin

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.db.models import Q
from ..utils import LimitOffsetPaginationWrapper
from ..serializers.base import SearchSerializer
from rest_framework.views import APIView
from core.models.socialMedia import UP_VOTE , DOWN_VOTE ,FAVORITE

class GenericSearchView(ListModelMixin , GenericAPIView):
    """ 
        generic search view for models that need search available fields are 
        [ text , path , tag ] for path search model must have a generic relations
        to core.LessonTree  and also a "get_by_path" method that handel path searching
        for tag search it should have a connection to taggit 
    """
    text_fields_search = []
    tag_field = 'tags'
    active_field = ['text' , 'path']
    serializer_class = None
    model = None
    pagination_class = LimitOffsetPaginationWrapper(20)

    def post(self,*args,**kwargs):
        return self.list(*args,**kwargs)

    def get_queryset(self): # data should serialize to check if thay are valid
        obj = self.model.objects.all() 
        request = self.request

        ### checking data 
        serializer = SearchSerializer(data = self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data_buf = serializer.data
        data = {}

        for field in self.active_field :
            if field in data_buf:
                data[field] = data_buf[field]
        
        if not data :
            raise ParseError('add one [ {} ] at least'.format(
                ' or '.join(self.active_field)))
        ### end checking


        if data.get('path' , None) :
            obj = self.lesson_tree_search_handler(data['path'] , self.model)

        if data.get('text' , None) :
            obj = self.text_fields_search_handler(data['text'] , obj)
        
        if data.get('tag' , None) :
            obj = self.tag_search_handler(data['tag'] , obj)
        
        return obj

    def text_fields_search_handler(self,text , obj):
        q = Q()
        for field in self.text_fields_search:
            for pattern in text.split():
                kwarg = {'{}__icontains'.format(field) : pattern}
                q |= Q( **kwarg )
        return obj.filter(q)

    def lesson_tree_search_handler(self,path , model):
        return model.get_by_path(path)
        
    def tag_search_handler(self , tag , obj):
        kwarg ={'{}__name__in'.format(self.tag_field) : tag }
        return obj.filter(**kwarg)


class GenericFeedbackView(APIView): 
    """ 
    generic feedback view for append voting futhure to models that use
    core.FeedBack as a vote save
    """
    allow_feedbacks = [UP_VOTE,DOWN_VOTE,FAVORITE]
    model = None
    feedback_field = 'votes'
    
    def post(self,request,quiz_pk):
        feedback_data = request.data.get('feedback_type',None)
        feedback_data = find_in_dict(feedback_data , FeedBack.FEEDBACK_TYPES)
        
        if not feedback_data and feedback_data not in self.allow_feedbacks:
            raise ParseError('uncorrect feedback , allow feedback(s) is {}'.format(
                ' ,'.join(self.allow_feedbacks)
            ))
        
        try:
            obj = model.objects.get(pk = quiz_pk)
        except ObjectDoesNotExist:
            raise ParseError('Quiz does not exist')
        
        try:# if user voted before , update it
            feedback = getattr(obj , self.feedback_field).get(user = request.user)
        except ObjectDoesNotExist:# if not create new 
            feedback = FeedBack(user = request.user, content_object = model) 

        feedback.feedback_type = feedback_data
        feedback.save()
        quiz.count_votes()
     
        return Response(data = 'feedback recoreded' , status = status.HTTP_200_OK)
