from django.conf.urls import url
from generics.view import method_splitter
from . import views
from .utils.emailAuth import activate
from django.views.generic import TemplateView
#from django.contrib.auth.views import  logout
from users.utils.temporary_keys_cleaner import cleaner

app_name = 'users'

urlpatterns = [
    #url(r'^login/$',
    #    login, {'template_name': 'login_form.html'},
    #    name='register'),
    #url(r'^logout/$', logout, {'template_name': 'logout_form.html'}),
    url(r'^signup/$', method_splitter, {
        'GET': views.register_GET,
        'POST': views.register_POST,
    }, name = 'signup'),
    url(r'^signup/successfully$',
        TemplateView.as_view(template_name='successfully_registration.html') 
        , name = 'sing_up_secc'),
    url(r'^activate/(?P<uidb64>[\d\w_\-]{1,5})/(?P<token>[\d\w]{1,13}-[\d\w]{1,30})/$',
        activate,
        name='activate'),
    url(r'^profile/$', views.profile_controller, name='profile_controller'),
    url(r'^profile/(?P<pk>\d+)/edit/$', views.ProfileEdit.as_view()),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view() , name = 'profile_view'),
]

#
#cleaner()
# this dont permit migration and makemigraions
# commands run correctly (for threading ) so clear hashtag when
# you want upload servies