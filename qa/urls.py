from django.conf.urls import url
from . import views

app_name = 'qa'

urlpatterns = [
    url(r'^$', views.QuestionListView.as_view(), name='index_noans'),
    url(r'^answered/$', views.QuestionAnsListView.as_view(), name='index_ans'),
    url(r'^lasts/$', views.QuestionsIndexListView.as_view(), name='index_all'),
    url(r'^question-detail/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^ask-question/$', views.CreateQuestionView.as_view(), name='ask_question'),
    url(r'^propose-answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='propose_answer'),
    #url(r'^qa/question/vote/$', views.QAHandler.as_view() ,{'_type': 'question'}, name='question_vote'),
    #url(r'^qa/answer/vote/$', views.QAHandler.as_view() , {'_type': 'answer'}, name='answer_vote'),
    #url(r'^qa/accept-answer/$', views.QAHandler.as_view() , {'_type':'accept_answer'}, name='accept_answer'),
]
