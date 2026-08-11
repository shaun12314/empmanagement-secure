from django.contrib import admin
from employee.models import Employee, Attendance, Notice, workAssignments, Requests

# Register your models here.
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Notice)
admin.site.register(workAssignments)
admin.site.register(Requests)