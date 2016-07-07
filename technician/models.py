from django.db import models
from django.core.validators import RegexValidator
from customerservice.models import Device

# Create your models here.

class Technician(models.Model):
    first_name = models.CharField(max_length = 120)
    middle_name = models.CharField(max_length = 120)
    last_name = models.CharField(max_length = 120)
    city = models.CharField(max_length = 50)
    area = models.CharField(max_length = 50)
    street = models.CharField(max_length = 50)
    block_number = models.SmallIntegerField()
    location_longitude = models.FloatField(blank = True, null = True)
    location_latitude = models.FloatField(blank = True, null = True)
    mobile_number = models.CharField(max_length = 11, unique = True, blank = True,\
                                     validators = [RegexValidator(r'\d{11}',"Please enter a valid mobile number.")])
    land_phone_number = models.CharField(max_length = 8, unique = True,\
                                    validators = [RegexValidator(r'\d{8}',"Please enter a valid phone number.")])

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


class Skill(models.Model):
    skill_name = models.CharField(max_length = 120)

    def __str__(self):
        return self.skill_name


class TechnicianSkill(models.Model):
    technician = models.ForeignKey(Technician, on_delete = models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete = models.CASCADE)
    years_of_exprience = models.SmallIntegerField()

    def __str__(self):
        return self.technician.__str__() + "\t" + self.skill.__str__()
