from __future__ import unicode_literals

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.exceptions import ValidationError

def send_email(email, username , token):
    me = 'amirhoseinbk00@gmail.com'  
    me_password = 'amir1380'
 
    msg = MIMEMultipart('alternative')
    msg['subject'] = "welcome to studylab"
    msg['to'] = email 
    msg['from'] = me

    text = """Hi! %s \n 
    whe are very happy of your join\n
    please open this link for complete your register :\n
    localhost:8000:/accounts/email_authenticate/%s""" %(username,token)
    html = """ 
    <html>
    <head></head>
        <body>
            <p>Hi! %s<br>
                How are you?<br>
                Here is the <a href='www.studylab.com/accounts/email_authenticate/%s'>localhost:8000:/accounts/email_authenticate/%s</a> you wanted.
            </p>
        </body>
    </html>
    """ %(username, token,token)
    part1 = MIMEText(text,'plain')
    part2 = MIMEText(html,'html')

    msg.attach(part1)
    msg.attach(part2)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(me, me_password)
        server.sendmail(me , msg['to'] , msg.as_string())
        server.close()
        return(1)
    except Exception, e:  
        raise ValidationError(e.message)

