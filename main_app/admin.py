from django.contrib import admin
from .models import ProcedureCategory, Procedure, ImageProcedure, ServiceProcedure, Schedule, ProcedureLimit, Record, Subscription, Customer

admin.site.register(ProcedureCategory)
admin.site.register(Procedure)
admin.site.register(ImageProcedure)
admin.site.register(ServiceProcedure)
admin.site.register(Schedule)
admin.site.register(ProcedureLimit)
admin.site.register(Record)
admin.site.register(Subscription)
admin.site.register(Customer)
# Register your models here.
