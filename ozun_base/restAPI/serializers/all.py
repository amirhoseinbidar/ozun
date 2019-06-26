from rest_framework import serializers
from quizzes.models import Answer ,Quiz , QuizStatus , Exam , Source 
from core.models import FeedBack , LessonTree ,TreeContent
from core.models import LessonTree ,allowed_types , GRADE , LESSON 
from rest_framework.exceptions import NotFound , NotAcceptable , ParseError
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from rest_auth.serializers import UserDetailsSerializer ,LoginSerializer
from ozun.settings import TIME_ZONE
from users.forms import ProfileForm
from ..utils import checkLessonTreeContent , checkSourceContent



class UserSerializer(UserDetailsSerializer):
    grade = serializers.CharField(source = 'profile.grade.full_path',required = False)
    interest_lesson = serializers.CharField(source = 'profile.interest_lesson.full_path',required = False)
    score = serializers.IntegerField(source = 'profile.score',read_only = True,required = False)
    bio = serializers.CharField(source = 'profile.bio',required = False)
    image = serializers.ImageField(source = 'profile.image' ,required = False)
    brith_day = serializers.DateField(source = 'profile.brith_day' , required = False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'grade' , 'interest_lesson' , 
            'score' , 'bio' , 'image' , 'brith_day' ,
        )
        extra_kwargs ={
            'username' : { 'read_only': True }
        }

    def update(self,instance,validated_data):
        profile_data = validated_data.pop('profile' , {})

        grade = profile_data.pop('grade',{}).pop('full_path' ,None)
        interest_lesson = profile_data.pop(
                'interest_lesson',{}).pop('full_path' ,None)
        
        instance = super(UserSerializer, self).update(instance, validated_data)
        profile = instance.profile
        profile_data['user'] = instance.pk

        if grade:
            profile_data['grade'] = checkLessonTreeContent(grade , GRADE , 'grade' ,False).pk
        if interest_lesson:
            profile_data['interest_lesson'] = checkLessonTreeContent(interest_lesson , LESSON , 'interest_lesson',  False).pk
    
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



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('quiz','is_correct_answer')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True )
    added_by = UserDetailsSerializer(many = False )
    lesson = serializers.CharField(source = 'lesson.full_path_slug')
    source = SourceSerializer(required = True)

    class Meta:
        model = Quiz
        fields = '__all__'
      

class QuizManagerSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many = True ,required=True)
    lesson = serializers.CharField(source = 'lesson.full_path_slug' ,required = True)
    source = serializers.CharField(source = 'source.name', required = True)

    def create(self,validated_data):
        answer_set = validated_data.pop('answer_set' , None)
        validated_data['lesson'] = validated_data.pop('lesson',{}).pop('full_path_slug',None)
        validated_data['lesson'] = checkLessonTreeContent(validated_data['lesson'],LESSON , 'lesson' )
        validated_data['source'] = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(validated_data['source'])
        quiz = Quiz.objects.create(**validated_data)

        for answer in answer_set:
            answer['quiz'] = quiz
            Answer.objects.create(**answer)
        
        return quiz

    def update(self,instance,validated_data): #TODO Update is very slow i should think about it 
        answer_set = validated_data.pop('answer_set' , None)
        validated_data['lesson'] = validated_data.pop('lesson',{}).pop('full_path_slug',None)
        validated_data['lesson'] = checkLessonTreeContent(validated_data['lesson'],LESSON , 'lesson' )
        validated_data['source'] = validated_data.pop('source',{}).pop('name',None)
        validated_data['source'] = checkSourceContent(validated_data['source'])
        
        Quiz.objects.filter(pk = instance.pk).update(**validated_data)
        Answer.objects.filter(quiz = instance).delete()# delete all previous answers 
        instance.refresh_from_db()

        for answer in answer_set: # add new answers
            answer['quiz'] = instance
            Answer.objects.create(**answer)
        
        return instance
    
    class Meta:
        model = Quiz
        fields = [
            'content'  ,'answer_set' , 'exponential_answer' ,  'lesson' , 'source' ,
            'level', 'time_for_out' , 'added_by' 
        ]
        extra_kwargs = {
            'added_by' : {'required' : True},
        }

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

class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeContent
        fields = '__all__'

class LessonSeializer(serializers.ModelSerializer):
    content = LessonContentSerializer()
    class Meta:
        model = LessonTree
        fields = ('content',)