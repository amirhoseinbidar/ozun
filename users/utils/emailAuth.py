from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.utils.token import account_activation_token
from ozun.settings import DEBUG
#from users.models import Email_auth ,Profile

def sendAuthEmail(request,user,to_email):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    }

    message = render_to_string('acc_active_email.html', context= context , request=request )

    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    
    #Email_auth().create_record(user = user)

    if DEBUG:
        context['mail'] = '\n{} \n {} \n to : {}\n'.format(
                    mail_subject,message,to_email)
        return context
    
    email.send()
    


