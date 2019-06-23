from rest_framework import serializers
from qa.models import Answer , Question 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            'total_votes' :{'read_only':True}
        }  

class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True ,required = False)
    class Meta:
        model = Question
        fields = '__all__'