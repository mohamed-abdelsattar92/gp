from django.contrib import admin
from .models import TechnicianUser, DispatcherUser, CustomerServiceUser
# Register your models here.


admin.site.register(TechnicianUser)
admin.site.register(DispatcherUser)
admin.site.register(CustomerServiceUser)
