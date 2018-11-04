import threading
from users.models import Email_auth , QuizzesInfo 
from quizzes.models import Quiz
from django.contrib.auth.models import User
from django.utils import timezone
from json import dumps ,loads
from datetime import datetime



# check email_auth and QuizzesInfo table
# and delete or disable who close_date of record is passed or key is not active 
class cleaner():
    def __init__(self):
        self.idleMood = False
        self.run_cleaner()

    def run_cleaner(self):   
        now = timezone.now()
        email_auth = Email_auth.objects.filter(close_date__lte = now) # get all of records that remove date is little or equal then now 
        quizzes_cache = QuizzesInfo.objects.filter(close_date__lte = now,is_active = True) # same
        
        self.idleMood = False
        if not email_auth.exists() and not quizzes_cache.exists() : #if still is not any thing
            self.idleMood = True 

        for record in email_auth:
            record.cleaner_action()

        for key in quizzes_cache:
            key.cleaner_action()

        if self.idleMood:
            threading.Timer(60.0, self.run_cleaner).start() # every 1 minute
        else:
            now = timezone.now()
            delay1 = timezone.timedelta(0,0)
            delay2 = timezone.timedelta(0,0)

            if quizzes_cache.exists():
                # return the littelest close_date and calculate delay time from now 
                delay1 = QuizzesInfo.objects.order_by('close_date')[0].close_date - now
            if email_auth.exists():
                delay2 = Email_auth.objects.order_by('close_date')[0].close_date - now 
            
            min_delay = delay2 #TODO:it is not right way 
            if delay1 < delay2 :
                min_delay = delay1

            threading.Timer(min_delay.seconds, self.run_cleaner).start()   

