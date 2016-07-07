from django.conf.urls import url
from authusers import views as authusers_views
from dispatcher import views as dispatcher_views


urlpatterns = [
    url(r'^login/$', authusers_views.dispatcher_login, name = "dispatcher_login"),
    url(r'^logout/$', authusers_views.dispatcher_logout, name = "dispatcher_logout"),
    url(r'^index/(\w+[._]*\w+)$', dispatcher_views.dispatcher_index, name = "dispatcher_index"),
    url(r'^view-tickets/$', dispatcher_views.dispatcher_view_tickets, name = "dispatcher_view_tickets"),
    url(r'^view-technicians/name/$', dispatcher_views.dispatcher_view_technicians_by_name,
        name = "dispatcher_view_technicians_by_name"),
    url(r'^view-technicians/skill/$', dispatcher_views.dispatcher_view_technicians_by_skill,
        name = "dispatcher_view_technicians_by_skill"),
    url(r'^view-technicians/location/$', dispatcher_views.dispatcher_view_technicians_by_location,
        name = "dispatcher_view_technicians_by_location"),
    url(r'^search-tech-skill/$', dispatcher_views.dispatcher_search_technician_by_skill,
        name = "dispatcher_search_technician_by_skill"),
    url(r'^assign-ticket$', dispatcher_views.dispatcher_assign_ticket, name = "dispatcher_assign_ticket"),
    # url(r'^reassign-technician/$', dispatcher_views.dispatcher_reassign_technician,
    #     name = "dispatcher_reassign_technician"),
    url(r'^reschedule-ticket$', dispatcher_views.dispatcher_reschedule_ticket,
        name = "dispatcher_reschedule_ticket")
]
