from django.conf.urls import url
from authusers import views as authusers_views
from customerservice import views as customerservice_views


urlpatterns = [
    url(r'^login/$', authusers_views.customer_service_login, name = "customer_service_login"),
    url(r'^logout/$', authusers_views.customer_service_logout, name = "customer_service_logout"),
    url(r'^index/(\w+[._]*\w+)$', customerservice_views.customer_service_index, \
        name = "customer_service_index"),
    url(r'^search/name$', customerservice_views.customer_service_search_by_name, \
        name = "customer_service_search_by_name"),
    url(r'^search/phone$', customerservice_views.customer_service_search_by_phone, \
        name = "customer_service_search_by_phone"),
]
