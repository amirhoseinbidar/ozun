from django.conf.urls import url,include
from rest_framework.authtoken.views import obtain_auth_token 
from . import views

urlpatterns = [
    url(r'^users/$',views.UserCreate.as_view(),name ='create_user'),
    url(r"^login/$", obtain_auth_token, name="login"),
    url(r"^quiz/(?P<action>\w{1,20})/$",views.QuizSearchList.as_view()),
    url(r'^quiz/(?P<action>\w{1,20})/(?P<From>\d{1,10}$)/(?P<To>\d{1,10}$)/'
        ,views.QuizSearchList.as_view()),
]