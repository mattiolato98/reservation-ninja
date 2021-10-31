from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['building__name', 'name']


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

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_('Lesson start time should be before end time'))
        return super(Lesson, self).clean()

    class Meta:
        ordering = ['day', 'start_time']


class Reservation(models.Model):
    link = models.URLField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return (
            f'{self.lesson.classroom.name} of {self.lesson.user.username} '
            f'from {self.lesson.start_time} to {self.lesson.end_time}'
        )

    class Meta:
        ordering = ['start_time', 'end_time']


class Log(models.Model):
    execution_time = models.FloatField()
    users = models.IntegerField()
    lessons = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.date}"

    @property
    def average_user_execution_time(self):
        return self.execution_time / self.users if self.users > 0 else 0

    @property
    def average_lesson_execution_time(self):
        return self.execution_time / self.lessons if self.lessons > 0 else 0


class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='feedbacks', null=True)
    ok = models.BooleanField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.ok}'