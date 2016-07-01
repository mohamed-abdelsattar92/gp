from django.conf.urls import url
from authusers import views as authusers_views
from dispatcher import views as dispatcher_views


urlpatterns = [
    url(r'^login/$', authusers_views.dispatcher_login, name = "dispatcher_login"),
    url(r'^logout/$', authusers_views.dispatcher_logout, name = "dispatcher_logout"),
    url(r'^index/(\w+[._]*\w+)$', dispatcher_views.dispatcher_index, name = "dispatcher_index")
]
