import threading
from users.models import email_auth 
from django.utils import timezone


# every 30 minute check email_auth  table
# and delete who remove_date of record is passed 
def run_cleaner():   
    now = timezone.now()
    records = email_auth.objects.all()
    for record in records:
        if record.remove_date < now:
            record.delete()
    threading.Timer(1800.0, run_cleaner).start()
