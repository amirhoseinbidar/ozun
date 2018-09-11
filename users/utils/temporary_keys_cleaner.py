import threading
from users.models import Email_auth , QuizzesInfo 
from quizzes.models import Quizzes
from django.contrib.auth.models import User
from django.utils import timezone
from json import dumps ,loads
from datetime import datetime



# every 1 minute check email_auth and temporary key table
# and delete who remove_date of record is passed or key is not active 
class cleaner():
    def __init__(self):
        self.idleMood = False
        self.run_cleaner()

    def run_cleaner(self):   
        now = timezone.now()
        email_auth = Email_auth.objects.filter(close_date__lte = now) # get all of records that remove date is little or equal then now 
        quizzes_cash = QuizzesInfo.objects.filter(close_date__lte = now) # same
        self.idleMood = False

           
        if not email_auth.exists() and not quizzes_cash.exists() : #if still is not any thing
            
            self.idleMood = True 

        for record in email_auth:
            record.user.delete() 
            record.delete()

        for key in quizzes_cash:
            quizzes_cash.disable()

        if self.idleMood:
            threading.Timer(60.0, self.run_cleaner).start() # every 1 minute
        else:
            now = timezone.now()
            delay1 = QuizzesInfo.objects.order_by('close_date')[0].remove_date - now
            delay2 = Email_auth.objects.order_by('close_date')[0].remove_date - now 
            
            min_delay = delay2 #TODO:it is not right way 
            if delay1 < delay2 :
                min_delay = delay1
            
            threading.Timer(min_delay.second, self.run_cleaner).start()   # return the littelest close_date and calculate delay time from now 

