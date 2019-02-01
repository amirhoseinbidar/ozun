from django.db import models
from django.dispatch import receiver 
from django.db.models.signals import pre_save
from core.checks import checkDuplicate
from django.core.exceptions import ObjectDoesNotExist

class Country_province(models.Model):
    
    name = models.CharField(max_length = 64)
    
    def __str__(self):
        return u'{0}'.format(self.name)
    
    def save(self,*args,**kwargs):
        checkDuplicate(Country_city,self,name = self.name)
        super(Country_province,self).save(*args,**kwargs)
    
    class Meta:
        db_table = "province"
class Country_county(models.Model):
    
    province = models.ForeignKey(Country_province , on_delete=models.CASCADE)
    name = models.CharField(max_length = 64)
    
    def __str__(self):
        return u'{0}/{1}'.format(self.province.name,self.name)
    
    def save(self,*args,**kwargs):
        checkDuplicate(Country_county,self,name = self.name)
        super(Country_county,self).save(*args,**kwargs)
    
    class Meta:
        db_table = "county"
class Country_city(models.Model):
    
    county = models.ForeignKey(Country_county, on_delete=models.CASCADE)
    name = models.CharField(max_length = 64)
        
    def __str__(self):
        return u'{0}/{1}/{2}'.format(
            self.county.province.name,self.county.name,self.name)

    def save(self,*args,**kwargs):
        checkDuplicate(Country_city,self,name = self.name)
        super(Country_city,self).save(*args,**kwargs)
        Location.objects.create(city = self)
    
    class Meta:
        db_table = "city"

    
class Location(models.Model):
    
    city = models.OneToOneField(Country_city ,on_delete=models.CASCADE)
    path = models.CharField(max_length=194)
    
    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.city.__str__()
        checkDuplicate(Location,self, path = self.path )
        
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


