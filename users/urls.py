from django.conf.urls import url
from general_views.view import method_splitter
from . import views
from .utils.emailAuth import activate
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from users.utils.temporary_keys_cleaner import cleaner

urlpatterns = [
    url(r'^login/$',
        login, {'template_name': 'login_form.html'},
        name='register'),
    url(r'^logout/$', logout, {'template_name': 'logout_form.html'}),
    url(r'^register/$', method_splitter, {
        'GET': views.register_GET,
        'POST': views.register_POST,
    }),
    url(r'^register/successfully$',
        TemplateView.as_view(template_name='successfully_registration.html')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate,
        name='activate'),
    url(r'^profile/$', views.profile_controller, name='profile_controller'),
    url(
        r'^profile/(?P<pk>\d{1,150})/edit/$', method_splitter, {
            'GET': views.profile_edit_GET,
            'POST': views.profile_edit_POST,
            'attr': 'pk'
        }),
    url(r'^profile/(?P<pk>\d{1,150})/$', views.profile, {'attr': 'pk'}),
]

#
#cleaner()
# this dont permit migration and makemigraions
# commands run correctly (for threading ) so clear hashtag when
# you want upload servies