from rest_framework import serializers
from quizzes.models import Answer ,Quiz , QuizStatus , Exam , Source 
from users.models import FeedBack
from studypost.models import  StudyPost 
from core.models import LessonTree ,allowed_types , GRADE , LESSON  , Location
from rest_framework.exceptions import NotFound , NotAcceptable , ParseError
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from rest_auth.serializers import UserDetailsSerializer ,LoginSerializer
from ozun.settings import TIME_ZONE
from users.forms import ProfileForm



class UserSerializer(UserDetailsSerializer):
    location = serializers.CharField(source = 'profile.location.path',required = False)
    grade = serializers.CharField(source = 'profile.grade.full_path',required = False)
    interest_lesson = serializers.CharField(source = 'profile.interest_lesson.full_path',required = False)
    score = serializers.IntegerField(source = 'profile.score',read_only = True,required = False)
    bio = serializers.CharField(source = 'profile.bio',required = False)
    image = serializers.ImageField(source = 'profile.image' ,required = False)
    brith_day = serializers.DateField(source = 'profile.brith_day' , required = False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'location', 'grade' , 'interest_lesson' , 
            'score' , 'bio' , 'image' , 'brith_day' ,
        )

    def update(self,instance,validated_data):
        profile_data = validated_data.pop('profile' , {})

        grade = profile_data.pop('grade',{}).pop('full_path' ,None)
        interest_lesson = profile_data.pop(
                'interest_lesson',{}).pop('full_path' ,None)
        location =  profile_data.pop('location',{}).pop('path' ,None)
        
        instance = super(UserSerializer, self).update(instance, validated_data)
        profile = instance.profile
        profile_data['user'] = instance.pk

        if grade:
            try:
                grade = LessonTree.find_by_path(grade)
                allowed_types(GRADE , grade,'grade')
                profile_data['grade'] = grade.pk 
            except ObjectDoesNotExist :
                raise NotFound('this grade is not exist')
            except ValidationError as e:
                raise NotAcceptable(e.message)
        if interest_lesson:
            try:
                interest_lesson = LessonTree.find_by_path(interest_lesson)
                allowed_types(LESSON ,  interest_lesson , 'interest_lesson')
                profile_data['interest_lesson'] =  interest_lesson.pk
            except ObjectDoesNotExist:
                raise NotFound('this grade is not exist')
            except ValidationError as e:
                raise NotAcceptable(e.message)

        if location:
            try:
                profile_data['location'] = Location.objects.get(path = location).pk
            except ObjectDoesNotExist:
                raise NotFound('this location is not exist')

        if 'image' in profile_data:
            form = ProfileForm( profile_data ,
                {'image': profile_data['image']} , instance = profile ) 
        else:
            form = ProfileForm(profile_data , instance=profile)
        if form.is_valid():
            form.save()
        else :
            raise ParseError(form.errors)
        return instance    


class StudyPostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = StudyPost

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True , required = True)
    added_by = UserDetailsSerializer(many = False , required = True)
    lesson = serializers.SerializerMethodField()
    source = SourceSerializer()
    
    def get_lesson(self,obj):
        data = None
        if obj.lesson:
            data = obj.lesson.full_path
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


