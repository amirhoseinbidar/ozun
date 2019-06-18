from django import forms
from .models import Profile 
from core.widget import DataListTextInput

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class profileEditForm(forms.Form):
    bio = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField()
    brith_day = forms.CharField( widget = forms.widgets.DateTimeInput(attrs= {'type':'date'}) )
    province = forms.CharField( widget = DataListTextInput() ) 
    county = forms.CharField( widget = DataListTextInput() )
    city = forms.CharField( widget = DataListTextInput() )
    grade = forms.CharField( widget = DataListTextInput() )
    interest_lesson = forms.CharField (widget = DataListTextInput() )
    
    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        profile =  Profile.objects.get(user = user)
        self.fields['first_name'].widget.attrs.update( {'value' :profile.user.first_name} ) 
        self.fields['last_name'].widget.attrs.update( {'value' : profile.user.last_name} ) 
        self.fields['bio'].widget.attrs.update( { 'value' : profile.bio } )
        self.fields['brith_day'].widget.attrs.update( { 'value' : profile.brith_day } ) 
        if profile.location:
            self.fields['province'].widget.attrs.update( { 'value' : profile.location.city.county.province.name } )
            self.fields['county'].widget.attrs.update( { 'value' : profile.location.city.county.name } )
            self.fields['city'].widget.attrs.update( { 'value' : profile.location.city.name } )
        if profile.grade: 
            self.fields['grade'].widget.attrs.update( { 'value' : profile.grade.content.name } )
        if profile.interest_lesson:
            self.fields['interest_lesson'].widget.attrs.update( { 'value' : profile.interest_lesson.content.name } )
        
        
    