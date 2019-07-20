from quizzes.models import Answer ,Quiz , QuizStatus , Source   
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from core.exceptions import duplicationException
from .base import LessonPathMixin , MediaGiverMixin 
from quizzes.models.models_quiz import  CHAPTER ,TOPIC ,LESSON
from ..utils import checkSourceContent


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('quiz',)
        extra_kwargs = {
            'is_correct_answer' : {'required' : True}
        }

class AnswerForExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('quiz' , 'is_correct_answer' )

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class QuizWithoutAnswerSerializer(LessonPathMixin ,serializers.ModelSerializer):
    answer_set = AnswerForExamSerializer( many = True )
    source = serializers.CharField(source = 'source.name')
    class Meta:
        model = Quiz
        fields = [
            'id' ,'content' , "answer_set"  ,  'lesson' , 
            'source' ,'level', 'time_for_out' , 'user' ,
        ]

class QuizManagerSerializer(
        LessonPathMixin ,
        MediaGiverMixin ,
        serializers.ModelSerializer):
    answer_set = AnswerSerializer( many = True ,required=True )
    source = serializers.CharField(source = 'source.name', required = True)
    allowed_types = [ LESSON , CHAPTER , TOPIC ]
    lesson_tree_field_required = True
    
    def create(self,validated_data):
        answer_set = validated_data.pop('answer_set' , None)
        self.check_answers(answer_set)

        validated_data['source'] = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(validated_data['source'])
        
        quiz = super().create(validated_data)

        for answer in answer_set:
            answer['quiz'] = quiz
            try:
                Answer(**answer).save()
            except duplicationException as e : 
                raise ParseError(e.message)
        
        return quiz

    def update(self,instance,validated_data):  
        answer_set = validated_data.pop('answer_set' , None)
        self.check_answers(answer_set)
        
        source = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(source)
        

        instance = super().update(instance , validated_data)
        instance.answer_set.all().delete()# delete all previous answers 
        instance.refresh_from_db()
        
        for answer in answer_set: # add new answers
            answer['quiz'] = instance       
            Answer(**answer).save()
            
                
        return instance
    
    def check_answers(self,answer_set):
        is_correct_count = 0
        for answer in answer_set:
            if answer['is_correct_answer']:
                is_correct_count += 1
        if is_correct_count == 0 :
            raise ParseError('please mark a answer as correct answer')
        if is_correct_count > 1 :
            raise ParseError('a quiz can not have two correct answer')

    class Meta:
        model = Quiz
        fields = [
            'id' , 'content'  ,'answer_set' , 'exponential_answer' ,  'lesson' , 'source' ,
            'level', 'time_for_out' , 'user' , 'total_votes' ,
        ]