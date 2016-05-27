from django.contrib import admin
from ticket.models import Ticket, TicketSolution, Visit, Schedule, ScheduleItem
from ticket.models import Category, PartName, ModelName, ActualPart


admin.site.register(Ticket)
admin.site.register(TicketSolution)
admin.site.register(Visit)
admin.site.register(Schedule)
admin.site.register(ScheduleItem)
admin.site.register(Category)
admin.site.register(PartName)
admin.site.register(ModelName)
admin.site.register(ActualPart)
