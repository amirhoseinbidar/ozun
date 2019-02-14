from django.conf.urls import url
from quizzes import views

urlpatterns =[
    url(r'^ask/$',views.ExamView.as_view()),
    url(r'^show_answer/$',views.ExamInformationView.as_view()),
]