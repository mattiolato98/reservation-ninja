from django.contrib import admin

from app.reservation_management.models import Classroom, Building, Lesson, Reservation, Log, Feedback

admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(Feedback)
admin.site.register(Lesson)
admin.site.register(Log)
admin.site.register(Reservation)
