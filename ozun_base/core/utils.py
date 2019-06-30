from .models import LessonTree

def find_in_dict(element, dictionary):
    for val in dictionary:
        if element == val[1] or element == val[0]:
            return val[0]
    return None

def get_all_related_lessonTree(model,model_field,lesson_path,get_by_slug):
        ''' get all objects that connent to lessont_path and its 
            sub branches objects '''
        branch = LessonTree.find_by_path(lesson_path , get_by_slug)
        lessons = list(branch.get_descendants())+[branch,]
        kwargs =  {'{}__in'.format(model_field) : lessons }
        obj = model.objects.filter( **kwargs )
        return obj