from django.db import models
from django.dispatch import receiver 
from django.db.models.signals import pre_save
from core.checks import checkDuplicate
from django.core.exceptions import ObjectDoesNotExist ,ValidationError 

from django.utils.text import slugify

class Country_province(models.Model):
    
    name = models.CharField(max_length = 65)
    slug = models.CharField(max_length = 65,blank = True)

    def __str__(self):
        return u'{0}'.format(self.name)
    
    def save(self,*args,**kwargs):
        checkDuplicate(Country_province,self,name = self.name)
        if not self.slug:
            self.slug = slugify(self.name , True)    
        super(Country_province,self).save(*args,**kwargs)
    
    class Meta:
        db_table = "province"


class Country_county(models.Model):

    province = models.ForeignKey(Country_province , on_delete=models.CASCADE)
    name = models.CharField(max_length = 65)
    slug = models.CharField(max_length = 65,blank = True)

    def __str__(self):
        return u'{0}/{1}'.format(self.province.name,self.name)
    
    def save(self,*args,**kwargs):
        checkDuplicate(Country_county,self,name = self.name)
        if not self.slug:
            self.slug = slugify(self.name , True)
        super(Country_county,self).save(*args,**kwargs)
    
    class Meta:
        db_table = "county"


class Country_city(models.Model):
    
    county = models.ForeignKey(Country_county, on_delete=models.CASCADE)
    name = models.CharField(max_length = 65)
    slug = models.CharField(max_length = 65,blank = True)
        
    def __str__(self):
        return u'{0}/{1}/{2}'.format(
            self.county.province.name,self.county.name,self.name)

    def save(self,*args,**kwargs):
        checkDuplicate(Country_city,self,name = self.name)
        if not self.slug:
            self.slug = slugify(self.name , True)
        super(Country_city,self).save(*args,**kwargs)
    
        if not Location.objects.filter(city = self).exists():
            Location.objects.create(city = self)


    class Meta:
        db_table = "city"

    
class Location(models.Model):
    
    city = models.OneToOneField(Country_city ,on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    path_slug = models.CharField(max_length = 255 ,blank = True)
    
    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.city.__str__()
        checkDuplicate(Location,self, path = self.path )
        
        if not self.path_slug:
            self.path_slug = '{}/{}/{}'.format(
                self.city.county.province.slug,self.city.county.slug,self.city.slug)

        super(Location,self).save(*args, **kwargs)
    
    def create_by_path(self,path_str): 
        pathes = path_str.split('/')
        province = self.get_or_create_state(Country_province,name = pathes[0])
        county = self.get_or_create_state(Country_county,
            name = pathes[1] , province = province)
        
        self.get_or_create_state(Country_city,
            name = pathes[2],county = county)
            
        return Location.objects.get(path = path_str)

    def get_or_create_state(self,klass,**kwargs):
        try:
            query = klass.objects.get(**kwargs)
            return query
        
        except ObjectDoesNotExist :
            query = klass(**kwargs)
            query.save()
            return query 
    
    #   I know this is a ugly wey but i will correct it later 
    #   i should change this to Tree mode like LessonTree
    @staticmethod
    def get_children(path_str , get_by_slug = False):
        if path_str.isspace() :
            raise ValidationError('path_str must not be empty')


        if get_by_slug:
            location_set = Location.objects.filter(path_slug__startswith = path_str)
        else:
            location_set = Location.objects.filter(path__startswith = path_str)
        print(location_set.values())
        if not location_set.exists():
            raise ObjectDoesNotExist()
        data = []
        for location in location_set:
            path_str = path_str.replace('-' , ' ')
            buf = location.path.replace(path_str , '').split('/')
            # there could be null list 
            try:
                #first index could be empty 
                data.append( buf[0] or buf[1] )
            except IndexError:
                raise ObjectDoesNotExist()

        # for break out duplicates
        data.sort()
        for ele in range(len(data)-1) :
            if ele == 0:
                continue
            if data[ele] == data[ele - 1]:
                del data[ele]

        return data

