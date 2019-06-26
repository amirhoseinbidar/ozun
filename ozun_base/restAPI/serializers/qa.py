from rest_framework import serializers
from qa.models import Answer , Question 
from .base import MediaGiverMixin


class AnswerSerializer(MediaGiverMixin , serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'total_votes' :{'read_only':True},
        }  

class QuestionSerializer(MediaGiverMixin , serializers.ModelSerializer ):
    answer_set = AnswerSerializer(many = True ,required = False ,read_only = True)
    
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'slug' :{'read_only':True},
            'user' :{'read_only':True},
            'has_answer':{'read_only':True},
            'total_votes' :{'read_only':True},
        }  