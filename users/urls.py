from django.conf.urls import url
from users import views
from general_views.view import template_loader
from django.contrib.auth.views import login , logout
from users.email_cleaner import run_cleaner

urlpatterns = [
    url(r'^login/$', login, {
        'template_name' : 'login_form.html' 
    }),

    url(r'^logout/$', logout, {
        'template_name' : 'logout_form.html'
    }),
    
    url(r'^register/$', views.method_splitter, {
        'GET': views.register_GET,
        'POST': views.register_POST
    }),
    url(r'^register/successfully$', template_loader,{
            'template_name': 'successfully_registration.html'
    }),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

run_cleaner()
