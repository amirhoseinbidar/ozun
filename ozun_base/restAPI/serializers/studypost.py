from rest_framework import serializers
from studypost.models import Course , Magazine ,CourseSubPost
from .base import MediaGiverMixin , LessonPathMixin


class MagazineSerializer(LessonPathMixin,MediaGiverMixin , serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'timestamp' :{'read_only':True},
            'slug' : {'read_only':True},
            'total_votes' : {'read_only':True}
        }  

class CourseSubPostSerializer(LessonPathMixin, MediaGiverMixin ,serializers.ModelSerializer):
    class Meta:
        model = CourseSubPost
        exclude = ('course',)

class CourseSerializer(LessonPathMixin, MediaGiverMixin ,serializers.ModelSerializer ):
    sub_posts = CourseSubPostSerializer(many = True)
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'timestamp' :{'read_only':True},
            'slug' : {'read_only':True},
            'total_votes' : {'read_only':True} , 
        }  
