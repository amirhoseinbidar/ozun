def make_ask_form(_quizzes):    
    ''' 
        NOTE:
            number index start from 1
            quiz is can be a object form Quizze model or quiz class

        you can send  a list to this function in three way
        first : [ quiz1, quiz2, quiz3, ... ]
        
        secound :[ {'quiz': quiz1, 'number':answer1} , {'quiz': quiz2, 'number':answer2} , ... ]
        
        or a mix  :[ quiz1 , {'quiz': quiz2, 'number':answer2} , ... ]
        
        numbe is a int number determain diffult checked answer if  you set " 'number':-1 " 
        or a number "out of range" function ignore and dont set diffult answer 
           
    '''
    quizzes = deepcopy(_quizzes)

    for _ in quizzes: # it is like a water stream every time we add a object in end should remove first object
        
        if isinstance(quizzes[0],dict):
            quizzes.append( Quiz(quizzes[0]['quiz'],int(quizzes[0]['answer'])) )
        elif isinstance(quizzes[0],Quiz):
            quizzes.append(quizzes[0])
        else:
            quizzes.append( Quiz(quizzes[0]) ) # add object to end 
        
        del quizzes[0] #  delete first object
    

    Forms =[]
    
    for quiz in quizzes:
        values = {}
        values['quiz'] = quiz.quiz.text
        list= quiz.quiz.answer.split('$$')# all answers store in a one string but every quistion seperate by these charecters
        answers_list =[]
        values['pk'] = quiz.quiz.pk
        i = 1
        for record in list:
            answer = { 'answer' : record, 'number' : i}
            if i == quiz.answer_number:
                answer['checked'] = True 

            answers_list.append(answer)
            i += 1
        values['answers'] = answers_list
        Forms.append(values)
    return Forms


#in must case we use of json and dictionary in same structure
#it is just a little class for make json data structure more butiful and pythonic
class Quiz: 
    def __init__(self,quiz = None,answer_number=-1):
        self.quiz = quiz
        self.answer_number = answer_number
    

    @staticmethod
    def dictToQuizClass(data):
        _quizData = Quizzes.objects.get(pk = data['quiz_pk'])#in json format we use of the id(pk) of quiz
        if 'answer_number' not in data:
            data['answer_number'] = -1
        return Quiz(_quizData , int(data['answer_number']) )#make sure answer is int 
    
    @staticmethod
    def dictListToQuizList(list):
        quizzes = []
        for data in list:
            quizzes.append(Quiz.dictToQuizClass(data))
        
        return quizzes
    
    @staticmethod
    def quizListTodict(quizList):
        data = []
        for quiz in quizList:
            data.append( {'pk' : quiz.quiz.pk ,'answer_number' : quiz.answer_number} )
        return data
    


# Create your models here.
class Grade(models.Model):   
    name = models.CharField(max_length= 30)
    # reverse ForeignKey 
    # same lesson can have diffrent grade  
 
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)
    def save(self , *args,**kwargs):
        checkDublicate(self.__class__ , self, name = self.name)
        super(self.__class__, self).save(*args,**kwargs)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Lesson(models.Model):
    chapter = models.ForeignKey('Chapter')
    
    name = models.CharField(max_length = 100)
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)
   
    def save(self , *args,**kwargs):
        checkDublicate(self.__class__ , self, name = self.name)
        super(self.__class__, self).save(*args,**kwargs)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Chapter(models.Model):
    #diffrent lesson can have same chapter
    grades = models.ManyToManyField(Grade)

    name = models.CharField(max_length = 100)
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)
    def save(self):
        checkDublicate(self.__class__ , self, name = self.name)
        return super(self.__class__, self).save()
    
    def __unicode__(self):
        return u'{0}'.format(self.name )


class Topic(models.Model):
    #but diffrent chapter can not have same chapter 
    grades = models.ManyToManyField(Grade)
    lessons = models.ManyToManyField(Lesson)
    chapter = models.ForeignKey(Chapter)

    name = models.CharField(max_length = 100)
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)    
    
    def save(self,*args,**kwargs):
        checkDublicate(self.__class__ , self, name = self.name)

        if self.chapter.lesson.pk != self.lesson.pk:
            raise unequalityException('Topic.lesson and chapter.lesson must be same')
        

        return super(self.__class__, self).save()
    
    def __unicode__(self):
        return u'{0}'.format(self.name )


#@receiver(m2m_changed,sender = Topic.grades.through)
#@receiver(m2m_changed,sender = Chapter.grades.through)
#def Quizzes_m2m_control(**kwargs): # for perform RULE 1 and 3
#    action = kwargs.pop('action', None)
#    instance = kwargs.pop('instance' , None)
#    sender = kwargs.pop('sender' , None)
#    
#    #NOTE: in signal methods if you raise a exception all data back to previous state     
#    if (action == 'post_add' or action == 'post_remove'):
#        
#        if sender is Chapter.grades.through:
#            lesson_grades = instance.lesson.grades.all()
#            print lesson_grades
#            if instance.grades.filter(pk__in = lesson_grades ).count() != instance.grades.all().count():
#                raise membershipException(message = 'all of Chapter.grade must be members of Chapter.lesson.grade')
#        
#        elif sender is Topic.grades.through:
#            chaptre_grades = instance.chapter.grades.all()
#            if instance.grades.filter(pk__in = chaptre_grades ).count() != instance.grades.all().count():
#                raise membershipException(message = 'all of Topic.grades must be members of Topic.chapter.grades')
     