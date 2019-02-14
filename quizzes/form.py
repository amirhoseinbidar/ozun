from django import forms
from core.widget import DataListTextInput

class examStartForm(forms.Form):
    grade = forms.CharField(widget = DataListTextInput())
    lesson = forms.CharField(widget = DataListTextInput())
    chapter = forms.CharField(widget = DataListTextInput() ,required=False )
    topic = forms.CharField(widget = DataListTextInput() ,required=False )
    source = forms.CharField(widget = DataListTextInput() ,required=False )
    level = forms.CharField(widget = DataListTextInput() ,required=False )
    number = forms.IntegerField(required=False)

    def get_lesson_path(self):
        path = '{}/{}'.format(self['grade'].value() , self['lesson'].value())
        print(path)
        if self['chapter'].value():
            path += '/'+ self['chapter'].value()
        if self['topic'].value():
            path += '/'+ self['topic'].value()
        return path