from rest_framework import serializers

from authusers.models import TechnicianUser
from technician.models import Technician


class TechnicianLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 120)
    password = serializers.CharField(max_length = 120)


class TechnicianLoginResponseSerializer(serializers.Serializer):
    technician_id = serializers.IntegerField()
    technician_exists = serializers.BooleanField()


class TechnicianLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ['location_longitude', 'location_latitude']


class TechnicianAllVisitsSerializer(serializers.Serializer):
    problem_description = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    date_of_visit = serializers.DateTimeField(read_only = True)
    ticket_id = serializers.IntegerField()
    visit_status = serializers.CharField(max_length = 10)


class TechnicianTodayVisitsSerializer(TechnicianAllVisitsSerializer):
    visit_order = serializers.IntegerField()


class TechnicianTicketSolution(serializers.Serializer):
    solution = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
