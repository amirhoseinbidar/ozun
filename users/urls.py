from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^login/$', views.method_splitter, {
        'GET': views.login_GET,
        'POST': views.login_POST
    }),

    url(r'^logout/$', views.method_splitter, {
        'GET': views.logout_GET,
    }),
    
    url(r'^register/$', views.method_splitter, {
        'GET': views.register_GET,
        'POST': views.register_POST
    }),
]