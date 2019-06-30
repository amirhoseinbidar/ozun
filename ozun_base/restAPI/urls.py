from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from . import views
from rest_auth.registration.urls import urlpatterns
from rest_auth.urls import urlpatterns
from rest_framework.routers import SimpleRouter

router = SimpleRouter()


router.register(r'qa/question' , views.QuestionViewSet , basename= 'qa_question' ) 
router.register(r'magazine' , views.MagazineViewSet, basename= 'mag' )
router.register(r'course', views.CourseViewSet , basename= 'cor' )
router.register(r'qa/answer' , views.AnswerViewSet , basename= 'qa_answer')

app_name = 'api'
urlpatterns = [


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


    url(r'^lesson/children/',
        views.LessonPathView.as_view(), name='lesson_path_view'),
    url(r'^sources/', views.SourceView.as_view(), name='source_view'),

    url(r'^exam/update/$', views.UpdateExam.as_view(), name='update_exam'),
    url(r'^exam/finish/$', views.FinishExam.as_view(), name='finish_exam'),
    url(r'^exam/info/(?P<exam_id>[\w\d]+)/$',
        views.ExamInfo.as_view(), name='exam_info'),
    url(r'^exam/start/(?P<LessonPath>[\w/-]+)',
        views.StartExam.as_view(), name='start_exam'),

    
    ###### tested #####
    
    url(r'^qa/question/answered/$', views.QuestionListView.as_view(),
        {'state': 'answered'} , name='qa_questions_ans'),
    url(r'^qa/question/unanswered/$', views.QuestionListView.as_view(),
        {'state': 'unanswered' } , name = 'qa_questions_unans' ),
  
  
    url(r'^qa/question/vote/$', views.QAHandler.as_view(),
        {'_type': 'question'}, name='question_vote'),
    url(r'^qa/answer/vote/$', views.QAHandler.as_view(),
        {'_type': 'answer'}, name='answer_vote'),
    url(r'^qa/accept-answer/$', views.QAHandler.as_view(),
        {'_type': 'accept_answer'}, name='accept_answer'),

    url(r'qa/question/search/',views.QuestionSearch.as_view()),

    url(r"magazine/search/", views.MagazineSearch.as_view() ),
    url(r"magazine/feedback/(?P<pk>\d+)/"  , views.MagzineFeedback.as_view() ),
    
    url(r"course/search/" ,views.CourseSearch.as_view() ),
    url(r"course/feedback/(?P<pk>\d+)/" ,views.CourseFeedback.as_view() ),
    #### tested ######
]

urlpatterns += router.urls