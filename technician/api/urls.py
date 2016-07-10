from django.conf.urls import url

from technician.api import views as api_views


urlpatterns = [
    url(r'^technician/(?P<tech_id>\d+)/update/location$', api_views.technician_update_location),
    url(r'^technician/login/$', api_views.technician_login),
    url(r'^technician/(?P<tech_id>\d+)/visits/today/$', api_views.technician_get_list_of_today_visits),
    url(r'^technician/(?P<tech_id>\d+)/visits/all/$', api_views.technician_get_list_of_all_visits),
    url(r'^technician/ticket/(?P<ticket_id>\d+)/solution$', api_views.technician_add_ticket_solution),
]
