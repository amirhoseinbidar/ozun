from rest_framework import serializers
from studypost.models import Course , Magazine 
from .base import MediaGiverMixin


class MagazineSerializer(MediaGiverMixin , serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'timestamp' :{'read_only':True},
            'lesson' : {'read_only':True}, #should not be readonly I will repair it
            'slug' : {'read_only':True},
            'votes' : {'read_only':True}
        }  

class CourseSerializer(MediaGiverMixin ,serializers.ModelSerializer ):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'user' :{'read_only':True},
            'timestamp' :{'read_only':True},
            'lesson' : {'read_only':True}, #should not be readonly I will repair it
            'slug' : {'read_only':True},
            'votes' : {'read_only':True}
        }  
