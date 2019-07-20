from rest_framework import serializers
from quizzes.models import Answer ,Quiz , QuizStatus , Exam
from ozun.settings import TIME_ZONE
from . import QuizWithoutAnswerSerializer , QuizManagerSerializer
from rest_framework.exceptions import ParseError

class QuizStatusSerializer(serializers.ModelSerializer):
    status_id = serializers.IntegerField(source = 'id')
    class Meta:
        model = QuizStatus
        exclude = ('exam','id')
        extra_kwargs = { 
            'quiz' : {'read_only' : True}  , 
        }

class QuizStatusWithoutAnswerSerializer(QuizStatusSerializer):
    quiz = QuizWithoutAnswerSerializer()

class QuizStatusWithAnswerSerializer(QuizStatusSerializer):
    quiz = QuizManagerSerializer()

class ExamStartSerializer(serializers.Serializer):
    level = serializers.ChoiceField(choices = Quiz.LEVEL_TYPE ,default=None, required = False)
    source = serializers.CharField(required = False ,default = None)
    number = serializers.IntegerField(required = False , default = None )
    path = serializers.CharField()

class ExamSerializer(serializers.ModelSerializer):
    quizstatus_set = QuizStatusSerializer( many = True )
    time_zone = serializers.SerializerMethodField()

    def get_time_zone(self,obj):
        return TIME_ZONE
    
    class Meta:
        model= Exam
        fields = ('id','close_date','add_date','time_zone' ,'quizstatus_set')
        extra_kwargs = {
            'close_date':{'read_only':True},
            'add_date':{'read_only':True},
        }
        
    def update(self,instance,validated_data):
        for status in  validated_data.pop('quizstatus_set'):
            print(status)
            quizStatus = instance.quizstatus_set.filter(id = status['id']) 
            if len(quizStatus) == 0:
                raise ParseError("status with id {} does not exist".format(status['id']))
            quizStatus = quizStatus[0]
            quizStatus.user_answer = status['user_answer']
            quizStatus.save()

        return instance

class ExamWithoutAnswerSerializer(ExamSerializer):
    quizstatus_set = QuizStatusWithoutAnswerSerializer(many =True )

class ExamWithAnswerSerializer(ExamSerializer):
    quizstatus_set = QuizStatusWithAnswerSerializer(many = True)