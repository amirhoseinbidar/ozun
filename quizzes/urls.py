from django.conf.urls import url
from generics.view import method_splitter
from quizzes import views

urlpatterns =[
    url(r'^ask/(?P<LessonPath>[\w/]+)$',views.ExamView.as_view()),
    url(r'^show_answer/$',views.ExamInformationView.as_view()),
]