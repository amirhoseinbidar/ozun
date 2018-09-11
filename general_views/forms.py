from django import forms

def find_datas(models, common_name, first_blank):
    """return a list of records
        models : a list of models data you want add .

        common_name : which attrebute (it use for all models ).

        first_blank : make a ['-1', '--------'] record in first of list .
    """ 

    info = []
    for records in models:
        array = []

        if first_blank:
            array.append(['-1', '--------'])

        info.append(array)

        for data in records:
            array.append([
                u'{0}'.format(data.pk), u'{0}'.format(getattr(data,common_name))
            ])
    
    return info

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)