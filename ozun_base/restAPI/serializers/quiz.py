from quizzes.models import Answer ,Quiz , QuizStatus , Source   
from rest_framework import serializers
from .base import LessonPathMixin , MediaGiverMixin 
from quizzes.models.models_quiz import  CHAPTER ,TOPIC ,LESSON
from ..utils import checkSourceContent

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('quiz',)

class AnswerForExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('quiz' , 'is_correct_answer' )

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class QuizForExamSerializer(serializers.ModelSerializer):
    answer_set = AnswerForExamSerializer( many = True )
    source = serializers.CharField(source = 'source.name')
    class Meta:
        model = Quiz
        fields = [
            'content' , "answer_set"  ,  'lesson' , 
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
        validated_data['source'] = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(validated_data['source'])
        
        quiz = super().create(validated_data)

        for answer in answer_set:
            answer['quiz'] = quiz
            Answer.objects.create(**answer)
        
        return quiz

    def update(self,instance,validated_data):  
        answer_set = validated_data.pop('answer_set' , None)
        source = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(source)
        
        instance = super().update(instance , validated_data)
        instance.answer_set.all().delete()# delete all previous answers 
        instance.refresh_from_db()

        for answer in answer_set: # add new answers
            answer['quiz'] = instance
            Answer.objects.create(**answer)
        
        return instance
    
    class Meta:
        model = Quiz
        fields = [
            'id' , 'content'  ,'answer_set' , 'exponential_answer' ,  'lesson' , 'source' ,
            'level', 'time_for_out' , 'user' , 'total_votes' ,
        ]