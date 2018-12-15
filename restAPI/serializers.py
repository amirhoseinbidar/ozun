from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from quizzes.models import Answer ,Quiz , QuizStatus , Exam
from users.models import Profile , FeedBack
from rest_framework.authtoken.models import Token
from course.models import StudyMedia , StudyPost , StudyPostBase
from core.models import LessonTree 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
        fields = ('username','password','email')
        extra_kwargs = {
            'password': {'write_only': True , 'required' : False}, 
            'email':{'required':True},
            'password':{'required':True}
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


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','is_staff')
        extra_kwargs = {
            'username' : {'read_only':True},
            'email':{'read_only':True},
            'is_staff': {'read_only':True},
        }

class ProfileSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(many=False)
    set_location  = serializers.CharField(max_length = 200,required = False)
    set_grade = serializers.CharField(max_length = 200,required = False)
    set_interest_lesson = serializers.CharField(max_length = 200,required = False)
    location  = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    interest_lesson = serializers.SerializerMethodField()

    def get_location(self,obj):
        pass 
 
    def get_interest_lesson(self,obj):
        data = None
        if obj.interest_lesson:
            data = obj.interest_lesson.turn_to_path()
        return data

    def get_grade(self,obj):
        data = None
        if obj.grade:
            data = obj.grade.turn_to_path()
        return data
        
    
    class Meta:
        model = Profile
        fields = '__all__'

        extra_kwargs ={
            'score' : {'read_only':True},
            'set_grade' : {'write_only' : True},
            'set_location': {'write_only' : True},
            'set_interest_lesson': {'write_only' : True},
        }
    

    def update(self,instance,validated_data):
        user_data = validated_data.pop('user',None)
        grade = validated_data.pop('set_grade',None)
        interest_lesson = validated_data.pop('set_interest_lesson',None)
        location = validated_data.pop('set_location',None)


        if grade:
            validated_data['grade'] = LessonTree.find_by_path(grade)
        if interest_lesson:
            validated_data['interest_lesson'] = LessonTree.find_by_path(interest_lesson)
        if location:
            validated_data['location'] = None # i will make it 
        User.objects.filter(pk = instance.user.pk).update(**user_data)

        Profile.objects.filter(pk = instance.pk).update(**validated_data)
        instance.refresh_from_db()
        
        return instance

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