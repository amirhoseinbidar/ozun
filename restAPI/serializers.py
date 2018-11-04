from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from quizzes.models import Answer ,Quiz
from users.models import Profile
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
        fields = ('id','username','password','email','first_name','last_name','is_staff')
        extra_kwargs = {
            'password': {'write_only': True}, 
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
    user = UserSerializer(many = False, required = True)
    class Meta:
        model = Profile
        fields = '__all__'

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
    
