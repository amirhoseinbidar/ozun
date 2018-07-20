import threading
from users.models import Email_auth 
from django.utils import timezone

# every 30 minute check email_auth  table
# and delete who remove_date of record is passed 
def run_cleaner():   
    now = timezone.now()
    records = Email_auth.objects.all()
    for record in records:
        if record.remove_date < now:
            record.delete()
    threading.Timer(600.0, run_cleaner).start()