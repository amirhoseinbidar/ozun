from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from quizzes.models import Answer ,Quiz , QuizStatus , Exam , Source 
from users.models import Profile , FeedBack
from rest_framework.authtoken.models import Token
from course.models import StudyMedia , StudyPost , StudyPostBase
from core.models import LessonTree ,allowed_types , GRADE , LESSON  , Location
from rest_framework.exceptions import NotFound , NotAcceptable
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from studylab.settings import TIME_ZONE

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

class ProfileSerializer(serializers.ModelSerializer): #i shuld make a custom field for this
    set_location  = serializers.CharField(max_length = 200,required = False)
    set_grade = serializers.CharField(max_length = 200,required = False)
    set_interest_lesson = serializers.CharField(max_length = 200,required = False)
    location  = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    interest_lesson = serializers.SerializerMethodField()

    def get_location(self,obj):
        if obj.location:
            return obj.location.path
 
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
        grade = validated_data.pop('set_grade',None)
        interest_lesson = validated_data.pop('set_interest_lesson',None)
        location = validated_data.pop('set_location',None)
        
        if grade:
            try:
                validated_data['grade'] = LessonTree.find_by_path(grade)
                allowed_types(GRADE , validated_data['grade'],'grade')
            except ObjectDoesNotExist :
                raise NotFound('this grade is not exist')
            except ValidationError as e:
                raise NotAcceptable(e.message)
        if interest_lesson:
            try:
                validated_data['interest_lesson'] = LessonTree.find_by_path(
                    interest_lesson)
                allowed_types(LESSON , validated_data['interest_lesson'] 
                    , 'interest_lesson')
            except ObjectDoesNotExist:
                raise NotFound('this grade is not exist')
            except ValidationError as e:
                raise NotAcceptable(e.message)

        if location:
            try:
                validated_data['location'] = Location.objects.get(path = location)
            except ObjectDoesNotExist:
                raise NotFound('this location is not exist')

        Profile.objects.filter(pk = instance.pk).update(**validated_data)
        instance.refresh_from_db()
        
        return instance

class StudyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('image',)
        model = StudyMedia

class StudyPostBaseSerializer(serializers.ModelSerializer):
    studymedia_set = StudyMediaSerializer(many = True)
    class Meta:
        fields = '__all__'
        model = StudyPostBase

class StudyPostSerializer(serializers.ModelSerializer):
    post = StudyPostBaseSerializer(many = False)
    class Meta:
        fields = ('post',)
        model = StudyPost

class AnswerSerializer(serializers.ModelSerializer):
    post = StudyPostBaseSerializer(many = True)
    class Meta:
        model = Answer
        fields = ('id','post','is_correct_answer')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True , required = True)
    added_by = UserSerializer(many = False , required = True)
    lesson = serializers.SerializerMethodField()
    source = SourceSerializer()
    
    def get_lesson(self,obj):#TODO:CODE_DUPLICATE with line 56
        data = None
        if obj.lesson:
            data = obj.lesson.turn_to_path()
        return data
    
    class Meta:
        model = Quiz
        fields = '__all__'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'

class QuizStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizStatus
        exclude = ('exam',)
class QuizStatusListSerializer(QuizStatusSerializer):
    quiz = QuizSerializer()
        
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
            #only one quiz_status is exist for each quiz in a exam
            quizStatus = instance.quizstatus_set.get(quiz = status['quiz']) 
            quizStatus.user_answer = status['user_answer']
            quizStatus.save()
        
        Exam.objects.filter(pk = instance.pk).update(**validated_data)
        instance.refresh_from_db()

        return instance

class ExamListSerializer(ExamSerializer):
    quizstatus_set = QuizStatusListSerializer(many =True)