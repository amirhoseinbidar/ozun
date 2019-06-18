from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from . import views
from rest_auth.registration.urls import urlpatterns
from rest_auth.urls import urlpatterns

app_name = 'api'
urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(
        r'^rest-auth/user/(?P<pk>\d+)/',
        views.userProfileList.as_view(),
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

    url(r'^quiz-manage/create/$', views.QuizCreate.as_view(), name='quiz_create'),
    url(r'^quiz-manage/update/(?P<pk>\d+)/$',
        views.QuizUpdate.as_view(), name='quiz_update'),

    url(r'^quiz/(?P<quiz_pk>\d)/feed-back/$',
        views.QuizFeedBack.as_view(), name='quiz_feed_back'),
    url(r"^quiz/(?P<action>[\w-]{1,20})/$",
        views.QuizSearchList.as_view(), name='search_quiz'),
    url(r'^quiz/(?P<action>[\w-]{1,20})/(?P<from>\d{1,10})/(?P<to>\d{1,10})/$',
        views.QuizSearchList.as_view(), name='search_selected_quiz'),
    url(r'^quiz/(?P<action>[\w-]{1,20})/(?P<pk>\d+)/$',
        views.QuizSearchList.as_view(), name='get_quiz'),
    url(r'^quiz/(?P<action>[\w-]{1,20})/(?P<LessonPath>[\w/-]+)',
        views.QuizSearchList.as_view(), name='search_lesson_path'),


    url(r'^lesson/children/(?P<LessonPath>[\w/-]+)',
        views.LessonPathView.as_view(), name='lesson_path_view'),
    url(r'^location/children/(?P<LocationPath>[\w/-]+)',
        views.LocationPathView.as_view(), name='location_path_view'),
    url(r'^sources/', views.SourceView.as_view(), name='source_view'),

    url(r'^exam/update/$', views.UpdateExam.as_view(), name='update_exam'),
    url(r'^exam/finish/$', views.FinishExam.as_view(), name='finish_exam'),
    url(r'^exam/info/(?P<exam_id>[\w\d]+)/$',
        views.ExamInfo.as_view(), name='exam_info'),
    url(r'^exam/start/(?P<LessonPath>[\w/-]+)',
        views.StartExam.as_view(), name='start_exam'),

    url(r'^qa/$', views.QuestionListView.as_view(), name='index_noans'),
    url(r'^qa/answered/$', views.QuestionAnsListView.as_view(), name='index_ans'),
    url(r'^qa/lasts/$', views.LastQuestionsView.as_view(), name='index_all'),
    url(r'^qa/question-detail/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^qa/ask-question/$', views.CreateQuestionView.as_view(), name='ask_question'),
    url(r'^qa/propose-answer/$',
        views.CreateAnswerView.as_view(), name='propose_answer'),
    url(r'^qa/question/vote/$', views.QAHandler.as_view(),
        {'_type': 'question'}, name='question_vote'),
    url(r'^qa/answer/vote/$', views.QAHandler.as_view(),
        {'_type': 'answer'}, name='answer_vote'),
    url(r'^qa/accept-answer/$', views.QAHandler.as_view(),
        {'_type': 'accept_answer'}, name='accept_answer'),

    url(r'^magzin/(?P<LessonPath>[\w/-]+)',
        views.StudyPostList.as_view(), name='magazine'),
    url(r'^source/(?P<LessonPath>[\w/-]+)',
        views.StudyPostList.as_view(), name='source'),
]
