from django.contrib import admin

from reservation_management.models import Classroom, Building, Timetable

admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(Timetable)
