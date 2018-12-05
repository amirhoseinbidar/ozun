from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from quizzes.models import Answer ,Quiz , QuizStatus , Exam
from users.models import Profile , FeedBack
from rest_framework.authtoken.models import Token
from course.models import StudyMedia , StudyPost , StudyPostBase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
        fields = ('id','username','password','email','first_name','last_name','is_staff')
        extra_kwargs = {
            'password': {'write_only': True , 'required' : False}, 
            'is_staff':{'read_only':True},
            'email':{'required':True}
            }
    def create(self,validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

        
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs ={
            'score' : {'read_only':True}
        }

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = ('id','text','is_correct_answer')

class QuizSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True , required = True)
    added_by = UserSerializer(many = False , required = True)
    class Meta:
        model = Profile
        fields = '__all__'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        models = FeedBack
        fields = '__all__'

class QuizStatusSerializer(serializers.ModelSerializer):
    class Meta:
        models = QuizStatus
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    quizstatus_set = QuizStatusSerializer(many = True )
    class Meta:
        models = Exam
        fields = ('id','is_active','user','quizstatus_set')
    
    def create(self,validated_data):
        quizzesStatus = validated_data.pop('quizstatus_set')
        exam = Exam.objects.create(**validated_data)
        for quizStatus in quizzesStatus:
            QuizStatus.objects.create(exam = exam , **quizStatus)
        return exam
    
    def update(self,instance,validated_data):
        quizzesStatus_data = validated_data.pop('quizstatus_set')
        quizzesStatus = (instance.quizstatus_set).all()
        quizzesStatus = list(quizzesStatus)
        instance.save()
        for quizstatus in quizzesStatus_data:
            status = quizstatus.pop(0)
            status.user_answer = quizzesStatus.get('user_answer',status.user_answer)
            status.save()
        return instance

class StudyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        models = StudyMedia

class StudyPostBaseSerializer(serializers.ModelSerializer):
    media = StudyMediaSerializer(many = True)
    class Meta:
        models = StudyPostBase

class StudyPostSerializer(serializers.ModelSerializer):
    post = StudyPostBaseSerializer(many = False)
    class Meta:
        models = StudyPost