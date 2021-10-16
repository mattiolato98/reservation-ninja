from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    WEEKDAYS = [
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
    ]
    day = models.PositiveSmallIntegerField(choices=WEEKDAYS, default=MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='lessons')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return (
            f'{self.user} in {self.classroom.name} - '
            f'{self.start_time.strftime("%H:%M")}/{self.end_time.strftime("%H:%M")} '
            f'on day {self.day}'
        )


class Reservation(models.Model):
    link = models.URLField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return (
            f'{self.lesson.classroom.name} of {self.lesson.user.username} '
            f'from {self.lesson.start_time} to {self.lesson.end_time}'
        )
