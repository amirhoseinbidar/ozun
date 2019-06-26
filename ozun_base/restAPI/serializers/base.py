
from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import ParseError
from core.exceptions import ValidationError

import re

class MediaGiverMixin(serializers.Serializer):
    media = serializers.ListField(write_only = True,required = False , 
                child = serializers.FileField( 
                max_length = 8000 , allow_empty_file = False , use_url = False))
   
    fields_search = ['content',] 
    

    def create(self,validated_data):
        return self.obj_save(validated_data  , None)
    
    def update(self , obj ,validated_data):
        return self.obj_save(validated_data , obj)
    

    def obj_save(self,validated_data , obj):
        media_buf = validated_data.pop('media',[])
        media = []
        validated_data['user'] = self.context['request'].user
        
        if obj:
            ###clearall media and reappend them 
            obj.media.all().delete()
            obj = super().update(obj , validated_data)
        else:
            obj = super().create(validated_data) 

        if not media_buf:
            obj.save()
            return obj

        

        for me in media_buf:
            media.append(
                obj.media.create(file = me , mime = me.content_type)
            )
        
        validated_data , obj = self.merge_media_and_text( validated_data , media , obj )
        obj.save()

        return obj 

    def merge_media_and_text(self, data , media , obj ):
        for container in self.fields_search: 
            txt = data.get(container,None)
            media_place = re.findall('{%%[\d ]*%%}',txt)
            for i in range(len(media_place)):
                ##get number
                n = int(re.findall('\d+',media_place[i])[0])
                
                # replace founded number with that media 
                print(media[n].file.url , '\n' ,media_place[i] )

                site = get_current_site(self.context['request'])
                
                txt = txt.replace(media_place[i] , site.domain+media[n].file.url )
                
            setattr(obj,container , txt)
        
        return (data,obj)
    
    def validate(self, data):
        numbers = []  
        for container in self.fields_search:
            txt = data.get(container,None)
            if not txt :
                raise ValidationError('{} do not exists in fields'.format(container))

            media_place = re.findall('{%%[\d ]*%%}',txt)

            for media_number in media_place:
                n = re.findall('\d+',media_number)
                if len(n) == 0: ## if there is no number in pattern
                    raise ParseError('uncorrect pattern: empty pattern is not allowed')
                if len(n) > 1: ## if we found more then one number
                    raise ParseError('uncorrect pattern: two number in one pattern is not allowed')
            
                numbers.append(n[0])
        
        numbers = list( dict.fromkeys(numbers) ) #clear duplicates
        
        if numbers and 'media' not in data:
            raise ParseError('uncorrect pattern: there is no matching media')

        for num in numbers:# is there a number that is not is media range?
            num  =  int(num)
            if num <= -1 or num >= len(data['media']):
                raise ParseError('uncorrect pattern: {} is out of media range'.format(num))

        return data