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
    