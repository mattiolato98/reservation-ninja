from django.contrib.auth import get_user_model
from django.db import models


class Log(models.Model):
    """
    Model that describe a Log object, it contains information about daily
    executions.
    """
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
        """
        This property returns a useful data about the average execution time of
        a lesson.

        Returns:
            float: average time resulted
        """
        return self.execution_time / self.lessons if self.lessons > 0 else 0


class Feedback(models.Model):
    """
    Model that describe a user feedback of the daily reservations.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='feedbacks', null=True)
    ok = models.BooleanField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.ok}'
