from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from users.utils.temporary_keys_cleaner import cleaner

app_name = 'users'


urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile_view_own'),
    url(r'^profile/edit/$', views.ProfileEdit.as_view(),name = 'profile_edit'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view() , name = 'profile_view'),
]

#
#cleaner()
# this dont permit migration and makemigraions
# commands run correctly (for threading ) so clear hashtag when
# you want upload servies
