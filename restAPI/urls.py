from django.conf.urls import url,include
from rest_framework.authtoken.views import obtain_auth_token 
from . import views

urlpatterns = [
    url(r'^users/$',views.UserCreate.as_view(),name ='create_user'),
    url(r"^login/$", obtain_auth_token, name="login"),
    url(r'^users/profile/$', views.ProfileUpdate.as_view() ,name = 'profile_update'),
    url(r'^users/profile/(?P<pk>\d)/$',views.ProfileView.as_view(),name = 'profile_view'),
    url(r"^quiz/(?P<action>\w{1,20})/$",views.QuizSearchList.as_view() , name = 'search_quiz'),
    url(r'^quiz/(?P<action>\w{1,20})/(?P<From>\d{1,10})/(?P<To>\d{1,10})/$'
        ,views.QuizSearchList.as_view(),name ='search_selected_quiz'),
    url(r'^quiz/(?P<action>\w{1,20})/(?P<LessonPath>[\w/]{1,100})' , 
        views.QuizSearchList.as_view() , name = 'search_lesson_path'),
    url(r'^quiz/(?P<pk>\d)/feed-back/$' , views.QuizFeedBack.as_view(), name = 'quiz_feed_back'),
    
    url(r'^exam/start/(?P<LessonPath>[\w/]{1,100})$' , views.StartExam , name='start_exam' ),
    url(r'^exam/update/$',views.UpdateExam.as_view(),name = 'update_exam'),
    url(r'^exam/(?P<pk>\d)/finish/$',views.FinishExam.as_view() ,name = 'finish_exam'),
    url(r'^exam/(?P<pk>[\d\w])/info/$',views.ExamInfo.as_view() , name = 'exam_info'),

    url(r'^studypost/(?P<LessonPath>[\w/]{1,100})$',views.StudyPostList.as_view() , name= 'study_post'),

]