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
    url(r'^to-add-device/$', customerservice_views.customer_service_to_add_device, \
        name = "customer_service_to_add_device"),
    url(r'^add-device/$', customerservice_views.customer_service_add_device,\
        name = "customer_service_add_device"),
    url(r'^add-customer/$', customerservice_views.customer_service_add_customer,\
        name = "customer_service_add_customer"),
    url(r'^to-add-ticket/$', customerservice_views.customer_service_to_add_ticket,\
        name = "customer_service_to_add_ticket"),
    url(r'^add-ticket/$', customerservice_views.customer_service_add_ticket,\
        name = "customer_service_add_ticket"),
]
