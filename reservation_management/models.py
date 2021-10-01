from django.contrib.auth import get_user_model
from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return self.name


class Timetable(models.Model):
    day = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='timetables')
