from rest_framework import serializers
from studypost.models import Course , Magazine 
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

class CourseSerializer(LessonPathMixin, MediaGiverMixin ,serializers.ModelSerializer ):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'timestamp' :{'read_only':True},
            'slug' : {'read_only':True},
            'total_votes' : {'read_only':True}
        }  
