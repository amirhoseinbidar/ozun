
from django.conf.urls import url
from generics.view import method_splitter
from quizzes import views

urlpatterns =[
    url(r'^ask/$',views.quizzes_ask_controller),
    url(r'^show_answer/$',views.quizzes_showAnswers_controller),
    url(r'^update_token/$',views.UpdateQuizzesInfo),
]