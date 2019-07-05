from rest_framework import serializers
from quizzes.models import Answer ,Quiz , QuizStatus , Exam , Source 
from core.models import FeedBack , LessonTree ,TreeContent
from core.models import LessonTree ,allowed_types , GRADE , LESSON 
from rest_framework.exceptions import NotFound , NotAcceptable , ParseError
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from rest_auth.serializers import UserDetailsSerializer 

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


class LessonSeializer(serializers.ModelSerializer):
    content = serializers.CharField(source = 'content.slug')
    class Meta:
        exclude = ("path",)
        model = LessonTree