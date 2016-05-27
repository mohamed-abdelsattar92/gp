from django.contrib import admin
from technician.models import Technician, Skill, TechnicianSkill


admin.site.register(Technician)
admin.site.register(TechnicianSkill)
admin.site.register(Skill)
