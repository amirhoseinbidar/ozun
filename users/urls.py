from django.conf.urls import url
from users import views
from django.views.generic import TemplateView
from django.contrib.auth.views import login , logout
from utils import run_cleaner

urlpatterns = [
    
    url(r'^login/$', login, {
        'template_name' : 'login_form.html' 
    } ,name = 'register'),

    url(r'^logout/$', logout, {
        'template_name' : 'logout_form.html'
    }),
    
    url(r'^register/$', views.method_splitter, {
        'GET': views.register_GET,
        'POST': views.register_POST,
    }),
    url(r'^register/successfully$', TemplateView.as_view(template_name='successfully_registration.html')),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$' , views.profile_controller , name = 'profile_controller'),
    url(r'^profile/(?P<username>.{1,150})/$' , views.profile) , # TODO: dot ' . ' is not secure
    
    url(r'^profile/(?P<username>.{1,150})/edit$',views.method_splitter,{
        'GET': views.profile_edit_GET,
        'POST': views.profile_edit_POST,
    })

]

run_cleaner()
