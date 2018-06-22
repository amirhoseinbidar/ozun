from django.conf.urls import url
from generics.view import method_splitter
from . import views
from .utils.emailAuth import activate
from django.views.generic import TemplateView
#from django.contrib.auth.views import  logout
from users.utils.temporary_keys_cleaner import cleaner

app_name = 'users'
  #url(r'^login/$',
    #    login, {'template_name': 'login_form.html'},
    #    name='register'),
    #url(r'^logout/$', logout, {'template_name': 'logout_form.html'}),
    
urlpatterns = [
    #url(r'^signup/$',views.SignUp.as_view(), name = 'sign_up'),
    #url(r'^signup/successfully$',
    #    TemplateView.as_view(template_name='successfully_registration.html') 
    #    , name = 'sign_up_succ'),
    #url(r'^activate/(?P<uidb64>[\d\w_\-]{1,5})/(?P<token>[\d\w]{1,13}-[\d\w]{1,30})/$',
    #    activate,
    #    name='activate'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile_view_own'),
    url(r'^profile/edit/$', views.ProfileEdit.as_view(),name = 'profile_edit'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view() , name = 'profile_view'),
]

#
#cleaner()
# this dont permit migration and makemigraions
# commands run correctly (for threading ) so clear hashtag when
# you want upload servies