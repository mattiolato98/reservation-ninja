from django.contrib import admin

from reservation_management.models import Classroom, Building, Lesson, Reservation

admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(Reservation)
