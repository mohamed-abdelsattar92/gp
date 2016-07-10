from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.db.models import Q

from ticket.models import Ticket, Schedule, ScheduleItem, Visit
from technician.models import TechnicianSkill, Skill, Technician
from dispatcher.forms import view_ticket_form, assign_ticket_form, view_technicians_form, re_forms


def dispatcher_index(request, username):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_index.html"
        context = dict()
        v_t_f = view_ticket_form.ViewTicketForm()
        v_tech_name = view_technicians_form.NameForm()
        v_tech_skill = view_technicians_form.SkillForm()
        v_tech_loc = view_technicians_form.LocationForm()
        context['username'] = username
        context['view_ticket_form'] = v_t_f
        context['view_tech_by_name'] = v_tech_name
        context['view_tech_by_skill'] = v_tech_skill
        context['view_tech_by_location'] = v_tech_loc
        return render(request, template, context)
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)


def dispatcher_view_tickets(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_view_tickets.html"
        context = dict()
        if request.POST:
            opened_tickets = list()
            assigned_tickets = list()
            work_in_progress_tickets = list()
            follow_up_tickets = list()
            form = view_ticket_form.ViewTicketForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                tickets = Ticket.objects.filter(Q(status = 'OP')|Q(status = 'AS')|Q(status = 'WP')|Q(status = 'FL'))
                for ticket in tickets:
                    if ticket.status == 'OP':
                        opened_tickets.append(ticket)
                    elif ticket.status == 'WP':
                        work_in_progress_tickets.append(ticket)
                    elif ticket.status == 'AS':
                        assigned_tickets.append(ticket)
                    else:
                        follow_up_tickets.append(ticket)
                    context['op'] = opened_tickets
                    context['as'] = assigned_tickets
                    context['wp'] = work_in_progress_tickets
                    context['fl'] = follow_up_tickets
                    context['opVal'] = f_c_d['opened']
                    context['asVal'] = f_c_d['assigned']
                    context['wpVal'] = f_c_d['work_in_progress']
                    context['flVal'] = f_c_d['follow_up']
                return render(request, template, context)
            else:
                return HttpResponse("form is invalid")
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)


def dispatcher_search_technician_by_skill(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_search_tech_by_skill.html"
        context = dict()
        if request.POST:
            technicians = list()
            skill_name = request.POST['search_skill']
            ticket_id = request.POST['ticket_pk']
            # if re assigning the ticket
            if request.POST.get('reassgin', None):
                request.session['reassign'] = True
            request.session['ticket_id'] = int(ticket_id)
            skill = Skill.objects.filter(skill_name__contains = skill_name)
            technicians_skills = TechnicianSkill.objects.filter(skill = skill)
            for tech_skill in technicians_skills:
                # get the technicians that have this certain skill
                tech = Technician.objects.get(pk = tech_skill.technician.pk)
                tech_schedule = Schedule.objects.get(technician = tech)
                tech_schedule_items = ScheduleItem.objects.filter(schedule = tech_schedule)
                technicians.append((tech, tech_schedule_items))
            context['technicians'] = technicians
            form = assign_ticket_form.AssignTicketForm()
            context['form'] = form
            return render(request, template, context)
        else:
            return HttpResponse("Not a post request")

    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)


def dispatcher_assign_ticket(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        if request.POST:
            form = assign_ticket_form.AssignTicketForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                # if reassigning the ticket
                if request.session.get('reassign', None):
                    old_ticket = Ticket.objects.get(pk = request.session.get('ticket_id'))
                    old_visit = Visit.objects.get(ticket_concerned = old_ticket)
                    old_schedule_item = ScheduleItem.objects.get(visit_concerned = old_visit)
                    old_visit.delete()
                    old_schedule_item.delete()
                    del request.session['reassign']
                # Ticket manipulation data
                technician = Technician.objects.get(pk = int(request.POST['tech_id']))
                ticket = Ticket.objects.get(pk = request.session.get('ticket_id'))
                ticket.status = 'AS'
                ticket.technician_resposible = technician
                # combining the date and time objects into one datetime object
                ticket.date_assigned = datetime.now()
                ticket.save()
                # creating a visit
                visit = Visit(
                    date_of_visit = datetime.combine(f_c_d['date_of_visit'], f_c_d['time_of_visit']),
                    longitude = ticket.device_concerned.customer.longitude,
                    latitude = ticket.device_concerned.customer.latitude,
                    ticket_concerned = ticket
                    )
                visit.save()
                # retreving Schedule of technician and Creating Schedule Item
                schedule = Schedule.objects.get(technician = technician)
                schedule_item = ScheduleItem(schedule = schedule, visit_concerned = visit)
                schedule_item.save()
                return HttpResponse("good job assigning tickets")
            else:
                return HttpResponse("not valid form data")
        else:
            return HttpResponse("Not post request")
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)
        # return HttpResponse("Assign Ticket View")


def dispatcher_view_technicians_by_name(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_view_technicians.html"
        context = dict()
        technicians_info = list()
        if request.POST:
            form = view_technicians_form.NameForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                technicians = Technician.objects.filter(
                    first_name__contains = f_c_d['first_name'],
                    middle_name__contains = f_c_d['middle_name'],
                    last_name__contains = f_c_d['last_name']
                )
                for tech in technicians:
                    tech_schedule = Schedule.objects.get(technician = tech)
                    tech_schedule_items = ScheduleItem.objects.filter(schedule = tech_schedule)
                    technicians_info.append((tech, tech_schedule_items))
                context['technicians_info'] = technicians_info
                return render(request, template, context)
            else:
                return HttpResponse("not valid form data")
        else:
            return HttpResponse("Not a post request")
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)


def dispatcher_view_technicians_by_skill(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_view_technicians.html"
        context = dict()
        technicians_info = list()
        technicians = list()
        if request.POST:
            form = view_technicians_form.SkillForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                skill_name = Skill.objects.get(skill_name__contains = f_c_d['skill'])
                technicians_skills = TechnicianSkill.objects.filter(skill = skill_name)
                for tech_skill in technicians_skills:
                    tech = Technician.objects.get(pk = tech_skill.technician.pk)
                    technicians.append(tech)
                for tech in technicians:
                    tech_schedule = Schedule.objects.get(technician = tech)
                    tech_schedule_items = ScheduleItem.objects.filter(schedule = tech_schedule)
                    technicians_info.append((tech, tech_schedule_items))
                context['technicians_info'] = technicians_info
                return render(request, template, context)
            else:
                return HttpResponse("not valid form data")
        else:
            return HttpResponse("Not a post request")
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)


def dispatcher_view_technicians_by_location(request):
    return HttpResponse("This is the view technician page")


def dispatcher_reschedule_ticket(request):
    dispatcher_user_id = request.session.get('dispatcher_user_id', None)
    dispatcher = request.session.get('dispatcher', None)
    if dispatcher_user_id and dispatcher:
        template = "dispatcher/dispatcher_reschedule_ticket.html"
        context = dict()
        if request.POST:
            form = re_forms.RescheduleForm(request.POST)
            if form.is_valid():
                f_c_d = form.cleaned_data
                ticket_id = request.session.get('ticket_id')
                ticket = Ticket.objects.get(pk = ticket_id)
                visit = Visit.objects.get(ticket_concerned = ticket)
                visit.date_of_visit = datetime.combine(f_c_d['date_of_visit'], f_c_d['time_of_visit'])
                visit.save()
                return HttpResponse("Good job rescheduling")
            else:
                return HttpResponse("not valid form data")
        else:
            request.session['ticket_id'] = int(request.GET.get('ticket_pk'))
            form = re_forms.RescheduleForm()
            context['form'] = form
            return render(request, template, context)
    else:
        response_redirect_url = reverse('dispatcher_login')
        return HttpResponseRedirect(response_redirect_url)
