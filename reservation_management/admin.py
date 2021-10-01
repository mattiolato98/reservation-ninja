from django.contrib import admin

from reservation_management.models import Classroom, Building

admin.site.register(Building)
admin.site.register(Classroom)
