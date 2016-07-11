from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError

from datetime import datetime
from datetime import time
from datetime import date
import urllib.request
import json

from technician.models import Technician
from authusers.models import TechnicianUser
from ticket.models import(
        Visit,
        TicketSolution,
        Ticket,
        ScheduleItem
        )

from technician.api.serializers import(
        TechnicianLocationSerializer,
        TechnicianLoginRequestSerializer,
        TechnicianLoginResponseSerializer,
        TechnicianAllVisitsSerializer,
        TechnicianTodayVisitsSerializer,
        TechnicianTicketSolution
        )


@api_view(['GET','PUT'])
def technician_update_location(request, tech_id):
    try:
        technician = Technician.objects.get(pk = int(tech_id))
    except Technician.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TechnicianLocationSerializer(technician, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        longg = float(request.query_params['long'])
        lat = float(request.query_params['lat'])
        technician.location_longitude = longg
        technician.location_latitude = lat
        technician.save()
        data = {'longitude-updated':'{0}'.format(longg),'latitude-updated':'{0}'.format(lat)}
        serializer = TechnicianLocationSerializer(technician, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.erros, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def technician_login(request):
    if request.method == 'POST':
        serializer = TechnicianLoginRequestSerializer(data = request.data)
        if serializer.is_valid():
            try:
                technician_user = TechnicianUser.objects.get(username = serializer.data['username'])
            except TechnicianUser.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
            if technician_user.check_password(serializer.data['password']):
                data = {
                    'technician_id': technician_user.technician_id.pk,
                    'technician_exists': True
                }
                serializer = TechnicianLoginResponseSerializer(data = data)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                data = {
                    'technician_id': -1,
                    'technician_exists':False
                }
                serializer = TechnicianLoginResponseSerializer(data = data)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def technician_get_list_of_today_visits(request, tech_id):
    if request.method == 'GET':
        try:
            technician = Technician.objects.get(pk = int(tech_id))
            serializer = None
        except Technician.DoesNotExist:
            return Response("This technician doesn't exist in the database isa")
        list_of_visits = Visit.objects.filter(technician_concerned = technician, date_of_visit__date = date.today())
        print(list_of_visits)
        if len(list_of_visits) > 2:
            waypoints_list = list()
            waypoints_dict = dict()
            google_api_url = "https://maps.googleapis.com/maps/api/directions/json?"
            for visit in list_of_visits:
                visit_lat_lng = str(visit.latitude) + ',' + str(visit.longitude)
                print(visit_lat_lng)
                waypoints_list.append(visit_lat_lng)
                waypoints_dict[visit_lat_lng] = visit

            # the start location is the location of the technician right now
            origin = str(technician.location_latitude) + ',' + str(technician.location_longitude)
            destination = origin
            google_api_url += "origin={0}&".format(origin)
            google_api_url += "destination={0}&".format(destination)
            google_api_url += "waypoints=optimize:true|"
            for waypoint in waypoints_list:
                google_api_url += "{0}|".format(waypoint)

            route =  urllib.request.urlopen(google_api_url)
            print(google_api_url)
            json_route = json.loads(route.read().decode(encoding='UTF-8')) # to change it from bytes to a string
            route_order = (json_route['routes'][0]['waypoint_order'])
            data_list = list()
            for i in range(len(list_of_visits)):
                visit = waypoints_dict[waypoints_list[route_order[i]]]
                data = {
                    'longitude': visit.longitude,
                    'latitude': visit.latitude,
                    'date_of_visit': visit.date_of_visit,
                    'problem_description': visit.ticket_concerned.problem_description,
                    'visit_status': visit.status,
                    'ticket_id': visit.ticket_concerned.pk,
                    'visit_order': i
                }
                data_list.append(data)
            serializer = TechnicianTodayVisitsSerializer(data = data_list, many = True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            data_list = list()
            for visit in list_of_visits:
                data = {
                    'longitude': visit.longitude,
                    'latitude': visit.latitude,
                    'date_of_visit': visit.date_of_visit,
                    'problem_description': visit.ticket_concerned.problem_description,
                    'ticket_id': visit.ticket_concerned.pk,
                    'visit_status': visit.status
                }
                data_list.append(data)

            serializer = TechnicianAllVisitsSerializer(data = data_list, many = True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def technician_get_list_of_all_visits(request, tech_id):
    if request.method == 'GET':
        try:
            technician = Technician.objects.get(pk = int(tech_id))
        except Technician.DoesNotExist:
            return Response("This technician doesn't exist in the database isa")
        list_of_visits = Visit.objects.filter(technician_concerned = technician, status = 'W')
        data_list = list()
        for visit in list_of_visits:
            data = {
                'longitude': visit.longitude,
                'latitude': visit.latitude,
                'date_of_visit': visit.date_of_visit,
                'problem_description': visit.ticket_concerned.problem_description,
                'ticket_id': visit.ticket_concerned.pk,
                'visit_status': visit.status
            }
            data_list.append(data)

        serializer = TechnicianAllVisitsSerializer(data = data_list, many= True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def technician_add_ticket_solution(request, ticket_id):
    if request.method == 'POST':
        serializer = TechnicianTicketSolution(data = request.data)
        if serializer.is_valid():
            try:
                ticket = Ticket.objects.get(pk = int(ticket_id))
                ticket.status = 'CL'
                ticket.device_concerned.last_maintenance_date = date.today()
                ticket.save()
            except Ticket.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                ticket_solution = TicketSolution(solution = serializer.data['solution'], ticket_concerned = ticket)
                ticket_solution.save()
            except IntegrityError:
                # return a conflict status if a solution already exists
                return Response('A ticket solution already exists', status=status.HTTP_409_CONFLICT)
            visit = Visit.objects.get(ticket_concerned = ticket)
            h, m, s = map(int, serializer.data['start_time'].split(':'))
            visit.start_time = time(h, m, s)
            h, m, s = map(int,serializer.data['end_time'].split(':'))
            visit.end_time = time(h,  m, s)
            visit.status = 'D'
            visit.save()
            schedule_item = ScheduleItem.objects.get(visit_concerned = visit)
            schedule_item.delete()
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
