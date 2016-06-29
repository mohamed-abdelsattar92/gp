from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    first_name = models.CharField(max_length = 120)
    middle_name = models.CharField(max_length = 120)
    last_name = models.CharField(max_length = 120)
    mobile_number = models.CharField(max_length = 11, unique = True, blank = True,\
                                     validators = [RegexValidator(r'\d{11}',"Please enter a valid mobile number.")])
    land_phone_number = models.CharField(max_length = 8, unique = True,\
                                    validators = [RegexValidator(r'\d{8}',"Please enter a valid phone number.")])
    address_formated = models.CharField(max_length = 200)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.first_name + "\t" + self.middle_name + "\t" + self.last_name


class Device(models.Model):
    model_name = models.CharField(max_length = 100)
    serial_number = models.BigIntegerField(unique = True)
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(null = True, blank = True)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.serial_number) + " " + self.customer.__str__()
