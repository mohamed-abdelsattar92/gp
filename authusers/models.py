import uuid
import hashlib
from django.db import models
from technician.models import Technician

# Create your models here.
class TechnicianUser(models.Model):
    username = models.CharField(max_length = 120, primary_key = True)
    password = models.CharField(max_length = 120)
    technician_id = models.OneToOneField(Technician, on_delete = models.CASCADE)

    def __str__(self):
        return self.username

    def hash_password(self):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + self.password.encode()).hexdigest() + ':' + salt

    def check_password(self, password):
        hash_password, salt = self.password.split(':')
        return hash_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.hash_password()
        super(TechnicianUser,self).save(*args, **kwargs)


class DispatcherUser(models.Model):
    username = models.CharField(max_length = 120, primary_key = True)
    password = models.CharField(max_length = 120)

    def __str__(self):
        return self.username

    def hash_password(self):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + self.password.encode()).hexdigest() + ':' + salt

    def check_password(self, password):
        hash_password, salt = self.password.split(':')
        return hash_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.hash_password()
        super(DispatcherUser,self).save(*args, **kwargs)


class CustomerServiceUser(models.Model):
    username = models.CharField(max_length = 120, primary_key = True)
    password = models.CharField(max_length = 120)

    def __str__(self):
        return self.username

    def hash_password(self):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + self.password.encode()).hexdigest() + ':' + salt

    def check_password(self, password):
        hash_password, salt = self.password.split(':')
        return hash_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.hash_password()
        super(CustomerServiceUser,self).save(*args, **kwargs)
