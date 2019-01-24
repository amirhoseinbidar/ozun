from django.conf.urls import url,include
from rest_framework.authtoken.views import obtain_auth_token 
from . import views


app_name = 'api'
urlpatterns = [
    url(r'^signup/$',views.UserCreate.as_view(),name ='create_user'),
    url(r"^login/$", obtain_auth_token, name="login"),
    
    url(r'^users/profile/$', views.ProfileUpdate.as_view() ,name = 'profile_update'),
    url(r'^users/profile/(?P<pk>\d)/$',views.ProfileView.as_view(),name = 'profile_view'),
    
    url(r'^quiz/(?P<quiz_pk>\d)/feed-back/$' , views.QuizFeedBack.as_view(), name = 'quiz_feed_back'),
    url(r"^quiz/(?P<action>[\w-]{1,20})/$",views.QuizSearchList.as_view() , name = 'search_quiz'),
    url(r'^quiz/(?P<action>[\w-]{1,20})/(?P<from>\d{1,10})/(?P<to>\d{1,10})/$'
        ,views.QuizSearchList.as_view(),name ='search_selected_quiz'),
    url(r'^quiz/(?P<action>[\w-]{1,20})/(?P<LessonPath>[\w/]+)' , 
        views.QuizSearchList.as_view() , name = 'search_lesson_path'),

    url(r'^exam/update/$',views.UpdateExam.as_view(),name = 'update_exam'),
    url(r'^exam/finish/$',views.FinishExam.as_view() ,name = 'finish_exam'),
    url(r'^exam/info/(?P<exam_id>[\w\d]+)/$',views.ExamInfo.as_view() , name = 'exam_info'),
    url(r'^exam/start/(?P<LessonPath>[\w/]+)' , views.StartExam.as_view() , name='start_exam' ),
    
    url(r'^qa/$', views.QuestionListView.as_view(), name='index_noans'),
    url(r'^qa/answered/$', views.QuestionAnsListView.as_view(), name='index_ans'),
    url(r'^qa/lasts/$', views.LastQuestionsView.as_view(), name='index_all'),
    url(r'^qa/question-detail/(?P<pk>\d+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
    #url(r'^qa/ask-question/$', views.CreateQuestionView.as_view(), name='ask_question'),
    #url(r'^qa/propose-answer/(?P<question_id>\d+)/$', views.CreateAnswerView.as_view(), name='propose_answer'),
    url(r'^qa/question/vote/$', views.QAHandler ,{'_type': 'question'}, name='question_vote'),
    url(r'^qa/answer/vote/$', views.QAHandler , {'_type': 'answer'}, name='answer_vote'),
    url(r'^qa/accept-answer/$', views.QAHandler , {'_type':'accept_answer'}, name='accept_answer'),

    url(r'^studypost/(?P<LessonPath>[\w/]+)',views.StudyPostList.as_view() , name= 'study_post'),

]
