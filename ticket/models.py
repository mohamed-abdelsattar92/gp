from django.db import models
from customerservice.models import Device
from technician.models import Technician


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('OP','Open'),
        ('AS', 'Assigned'),
        ('WP', 'Work In Progress'),
        ('FL','Need Follow Up'),
        ('CL', 'Closed'),
    )
    problem_title = models.CharField(max_length = 100)
    problem_description = models.TextField()
    date_opened = models.DateTimeField(auto_now_add = True)
    date_assigned = models.DateTimeField(null = True, blank = True)
    date_solved = models.DateTimeField(null = True, blank = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'OP')
    technician_resposible = models.ForeignKey(Technician, on_delete = models.SET_NULL, blank = True, null = True)
    device_concerned = models.ForeignKey(Device, on_delete = models.CASCADE)

    def __str__(self):
        return self.problem_title + "\t" + self.device_concerned.__str__()

    def get_technician_name(self):
        return self.technician_resposible.__str__()


class TicketSolution(models.Model):
    solution = models.TextField()
    case_close_date = models.DateTimeField(auto_now_add = True)
    ticket_concerned = models.OneToOneField(Ticket, on_delete = models.CASCADE)
    problem_description = models.TextField(blank = True)
    # Just for building the knowldedge base for later AI

    def __str__(self):
        return self.ticket_concerned.__str__()

    def get_problem_description(self):
        return self.ticket_concerned.problem_description

    # Here we're overiding the save method of the class Model to make the problem_description comes from the
    # ticket_concerned value problem_description :D :D (ana fa5or b nafsi fil 7ita deh ya3ni B| B|)
    def save(self, *args, **kwargs):
        self.problem_description = self.ticket_concerned.problem_description
        super(TicketSolution,self).save(*args, **kwargs)


class Visit(models.Model):
    STATUS_CHOICES = (
        ('W', 'Waiting'),
        ('D', 'Done'),
    )
    date_of_visit = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_time = models.TimeField(blank = True, null = True)
    end_time = models.TimeField(blank = True, null = True)
    ticket_concerned = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    technician_concerned = models.ForeignKey(Technician, on_delete = models.CASCADE, blank = True, null = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'W')

    def __str__(self):
        return str(self.date_of_visit) + self.ticket_concerned.__str__()

    def save(self, *args, **kwargs):
        self.technician_concerned = self.ticket_concerned.technician_resposible
        super(Visit,self).save(*args, **kwargs)


class Schedule(models.Model):
    name_of_technician = models.CharField(max_length = 120, blank = True)
    technician = models.OneToOneField(Technician, on_delete = models.CASCADE)

    def __str__(self):
        return self.name_of_technician

    def save(self, *args, **kwargs):
        self.name_of_technician = self.technician.__str__()
        super(Schedule,self).save(*args, **kwargs)


class ScheduleItem(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE)
    visit_concerned = models.OneToOneField(Visit, on_delete = models.CASCADE)
    longitude = models.FloatField(blank = True)
    latitude = models.FloatField(blank = True)
    date_of_visit = models.DateTimeField(blank = True)

    def __str__(self):
        return self.visit_concerned.technician_concerned.__str__()

    def save(self, *args, **kwargs):
        self.longitude = self.visit_concerned.longitude
        self.latitude = self.visit_concerned.latitude
        self.date_of_visit = self.visit_concerned.date_of_visit
        super(ScheduleItem,self).save(*args, **kwargs)


# Spare-Parts classes
class Category(models.Model):
    category_name = models.CharField(max_length = 120)

    def __str__(self):
        return self.category_name


class ModelName(models.Model):
    model_name = models.CharField(max_length = 120)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.model_name + "\t" + self.category.__str__()

    def get_category_name(self):
        return self.category.category_name


class PartName(models.Model):
    part_name = models.CharField(max_length = 120)
    quantity = models.SmallIntegerField()
    in_stock = models.BooleanField(default = True)
    model_name = models.ForeignKey(ModelName, on_delete = models.CASCADE)

    def __str__(self):
        return self.part_name + "\t" + self.model_name.__str__()

    def get_model_name(self):
        return self.model_name.model_name


class ActualPart(models.Model):
    serial_number = models.BigIntegerField()
    part_name = models.ForeignKey(PartName, on_delete = models.CASCADE)
    ticket_concerned = models.ForeignKey(Ticket, on_delete = models.CASCADE)

    def __str__(self):
        return self.part_name.__str__() + "\t" + str(self.serial_number)

    def get_part_name(self):
        return self.part_name.part_name
