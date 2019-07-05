from rest_framework import serializers
from quizzes.models import Answer ,Quiz , QuizStatus , Exam
from ozun.settings import TIME_ZONE
from . import QuizForExamSerializer

class QuizStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizStatus
        exclude = ('exam',)

class QuizStatusListSerializer(QuizStatusSerializer):
    quiz = QuizForExamSerializer()
      

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
            quizStatus = instance.quizstatus_set.get(id = status['status_id']) 
            quizStatus.user_answer = status['user_answer']
            quizStatus.save()

        return instance

class ExamListSerializer(ExamSerializer):
    quizstatus_set = QuizStatusListSerializer(many =True)

