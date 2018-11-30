from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.utils.token import account_activation_token
from studylab.settings import DEBUG

def sendAuthEmail(request,user,to_email):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
  
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    })
    
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    if DEBUG:
        print('\n{} \n {} \n to : {}\n'.format(mail_subject,message,to_email))
        return

    email.send()

from django.contrib.auth.models import User
from users.models import Email_auth, Profile 
from django.contrib.auth import login
from django.http import HttpResponse , HttpResponseRedirect
def activate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        #when record timeout in Email auth end we clear user and email auth so
        # if user cleared this function raise error  
    except :
        user = None
    
    if user is not None and account_activation_token.check_token(user, token) :
        user.is_active = True
        user.save()
        Profile(user =user).save()
        Email_auth.objects.get(user = user).delete()
        login(request,user)

        return HttpResponseRedirect('/accounts/profile')
    else:
        text = 'Activation link is invalid or out of date! please register again' 
        return HttpResponse(text)