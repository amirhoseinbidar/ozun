"""ozun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic import TemplateView
from ozun import settings
from quizzes.admin import quizzesAdminSite
from restAPI.views import userProfileList

app_name = 'ozun'

urlpatterns = [
    url(r'^$' , TemplateView.as_view(template_name = 'index.html'),name = 'index'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(
        r'^rest-auth/user/(?P<pk>\d+)/',
        userProfileList.as_view(),
        name='user_profile_list'
    ),
    #url(
    #    r'^socialaccounts/$',
    #    SocialAccountListView.as_view(),
    #    name='social_account_list'
    #),
    #url(
    #    r'^socialaccounts/(?P<pk>\d+)/disconnect/$',
    #    SocialAccountDisconnectView.as_view(),
    #    name='social_account_disconnect'
    #),
    
    url(r'^api/',include('restAPI.urls')),
    #url(r'^accounts/', include('users.urls')),  
    #url(r'^quizzes/',include('quizzes.urls')),
    #url(r'qa/',include('qa.urls')),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/users/', admin.site.urls),
    url(r'^admin/quizzes/',quizzesAdminSite.urls),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
