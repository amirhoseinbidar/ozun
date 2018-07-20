from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile ,Country_province, Country_county, Country_city
from general_views.forms import ListTextWidget ,find_datas




class registerForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(
        max_length=254, widget=forms.PasswordInput, label='password')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('A user with that email already exists.')
       
        return email


 


#class ListTextFields(forms.ModelForm):
#    def __inti__(self,*args,**kwargs):
#        data_dict = kwargs.pop('data_list',None)
#        super(ListTextFields,self).__init__(*args,**kwargs)
#        for field in data_dict:
#            self.fields['{0}'.format(field['name'])] = ListTextWidget(data_list= field['data'], name = field['name'])
#
class profileEditForm(forms.ModelForm):
    
    models = [
        Country_province.objects.all(),
        Country_county.objects.all(),
        Country_city.objects.all(),
    ]
    data = find_datas(models, 'name', True)
    ####notice :I am wondered between these two code
    ####
    #provinces_list = [value for key, value in data[0] ]
    #counties_list = [value for key, value in data[1] ]
    #cities_list = [value for key, value in data[2] ]
    #provinces_field = forms.CharField(
    #    widget=ListTextWidget(data_list=provinces_list,name='provinces_list'),required=False, label='province')
    #counties_field = forms.CharField(
    #    widget=ListTextWidget(data_list=counties_list,name='counties_list'),required=False, label='county')
    #cities_field = forms.CharField(
    #    widget=ListTextWidget(data_list=cities_list,name='cities_list'),required=False, label='city')
      
    provinces_field = forms.CharField(
       widget=forms.Select(choices=data[0]),required=False, label='province')
    counties_field = forms.CharField(
        widget=forms.Select(choices=data[1]),required=False, label='county')
    cities_field = forms.CharField(
        widget=forms.Select(choices=data[2]),required=False, label='city')
        
    first_name = forms.CharField(max_length=254,required=False)
    last_name = forms.CharField(max_length=254,required=False)
    years = [i + 1 for i in range(1950, 2018)]
    brith_day = forms.DateField(widget=forms.SelectDateWidget(years=years),required=False)
    test= forms.ChoiceField(widget = forms.RadioSelect , choices = [['1','<i>hello</i>'],['2','<strong>two</strong>']])

    class Meta:
        model = Profile
        fields = ('image', 'bio', 'brith_day','grade','interest_lesson')