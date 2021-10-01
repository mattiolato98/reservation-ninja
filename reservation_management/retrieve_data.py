from django.contrib.auth import get_user_model
from numpy import less
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd

from reservation_management.models import Building, Classroom, Timetable
from user_management.models import PlatformUser


PASSWD_FILE = ".credentials"
CLASS_SCHEDULE_FILE = 'class_schedule.csv'
URL = "https://www.unimore.it/covid19/trovaaula.html"


def get_credentials(text_file):
    with open(text_file, 'r') as f:
        lines = (line.rstrip() for line in f.readlines())
        credentials = dict(zip(["username", "password"], lines))
    
    return credentials


def get_building_from_classroom(classroom):
    return 'Fisica' if classroom[0] == 'L' else 'Matematica'


def get_lesson_metadata(lecture):
    return [lecture.classrom.name, lecture.start_time, lecture.end_time, lecture.classroom.building]


def get_day_schedule(day_idx, user):
    keys_list = ["classroom", "start_time", "end_time", "building"]
    lectures = Timetable.objects.get(day=day_idx, user=user)
    day_schedule = [dict(zip(keys_list, get_lesson_metadata(lecture)))
                    for lecture in lectures]
    return day_schedule


if __name__ == "__main__":
    credentials = get_credentials(PASSWD_FILE)
    day_idx = str(datetime.today().weekday())

    for user in get_user_model().objects.all():
        day_schedule = get_day_schedule(day_idx, user)
        # TODO: ripartire da qui dopo aver preso l'orario del giorno ed aver creato un dizionario.