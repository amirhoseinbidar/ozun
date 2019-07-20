from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from . import views
from rest_auth.registration.urls import urlpatterns
from rest_auth.urls import urlpatterns
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'qa/question' , views.QuestionViewSet , basename= 'qa-question' ) 
router.register(r'qa/answer' , views.AnswerViewSet , basename= 'qa-answer')
router.register(r'magazine', views.MagazineViewSet, basename= 'mag' )
router.register(r'course', views.CourseViewSet , basename= 'cor' )
router.register(r'quiz', views.QuizManagerViewSet ,basename= 'quiz-manage' )

urlpatterns = [
    url(r'^lesson/children/',
        views.LessonPathView.as_view(), name='lesson_path_view'),

    url(r'^sources/', views.SourceView.as_view(), name='source_view'),

    url(r'^quiz/feed-back/(?P<pk>\d)/$',
        views.QuizFeedBack.as_view(), name='quiz_feed_back'),
    url(r"quiz/search/", views.QuizSearchContent.as_view() ),
    url(r"quiz/most-vote/", views.QuizMostVote.as_view() ),

    url(r'^exam/start/',
        views.StartExam.as_view(), name='start_exam'),
    url(r'^exam/update/$', views.UpdateExam.as_view(), name='update_exam'),
    url(r'^exam/finish/$', views.FinishExam.as_view(), name='finish_exam'),
    url(r'^exam/info/(?P<exam_id>[\w\d]+)/$',
        views.ExamInfo.as_view(), name='exam_info'),
   
    
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
]

urlpatterns += router.urls
