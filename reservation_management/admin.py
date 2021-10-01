from django.contrib import admin

from reservation_management.models import Classroom, Building, Lesson

admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(Lesson)
