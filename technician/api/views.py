from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError

from datetime import datetime
from datetime import time


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
        TechnicianVisitsSerializer,
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
def technician_get_list_of_visits(request, tech_id):
    if request.method == 'GET':
        try:
            technician = Technician.objects.get(pk = int(tech_id))
        except Technician.DoesNotExist:
            return Response("This technician doesn't exist in the database isa")
        list_of_visits = Visit.objects.filter(technician_concerned = technician)
        data_list = list()
        for visit in list_of_visits:
            data = {
                'longitude': visit.longitude,
                'latitude': visit.latitude,
                'date_of_visit': visit.date_of_visit,
                'problem_description': visit.ticket_concerned.problem_description,
                'ticket_id': visit.ticket_concerned.pk
            }
            data_list.append(data)

        serializer = TechnicianVisitsSerializer(data = data_list, many= True)
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
                ticket.save()
            except Ticket.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                ticket_solution = TicketSolution(solution = serializer.data['solution'], ticket_concerned = ticket)
                ticket_solution.save()
            except IntegrityError:
                # return a conflict status if a solution already exists
                return Response('A ticket already exists', status=status.HTTP_409_CONFLICT)
            visit = Visit.objects.get(ticket_concerned = ticket)
            h, m, s = map(int, serializer.data['start_time'].split(':'))
            visit.start_time = time(h, m, s)
            h, m, s = map(int,serializer.data['end_time'].split(':'))
            visit.end_time = time(h,  m, s)
            visit.save()
            schedule_item = ScheduleItem.objects.get(visit_concerned = visit)
            schedule_item.delete()
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
