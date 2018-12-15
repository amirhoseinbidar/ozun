from django.db import models
from django.dispatch import receiver 
from django.db.models.signals import pre_save
from core.checks import checkDuplicate

class Country_province(models.Model):
    name = models.CharField(max_length = 64)
    class Meta:
        db_table = "province"
    def __str__(self):
        return u'{0}'.format(self.name)

class Country_county(models.Model):
    province = models.ForeignKey(Country_province , on_delete=models.CASCADE)
    name = models.CharField(max_length = 64)
    class Meta:
        db_table = "county"
    def __str__(self):
        return u'{0}/{1}'.format(self.province.name,self.name)

class Country_city(models.Model):
    county = models.ForeignKey(Country_county, on_delete=models.CASCADE)
    name = models.CharField(max_length = 64)
    class Meta:
        db_table = "city"
        
    def __str__(self):
        return u'{0}/{1}/{2}'.format(
            self.county.province.name,self.county.name,self.name)

    def save(self,*args,**kwargs):
        super(Country_city,self).save(*args,**kwargs)
        Location.objects.create(city = self)

class Location(models.Model):
    city = models.OneToOneField(Country_city ,on_delete=models.CASCADE)
    path = models.CharField(max_length=194)
    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.city.__str__()

        checkDuplicate(Location,self, path = self.path )
        
        super(Location,self).save(*args, **kwargs)
    

