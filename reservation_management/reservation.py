from os.path import dirname

import django
import os
import sys
from time import time as measure_time
from datetime import datetime
from datetime import time

import pytz
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

PROJECT_PATH = os.path.join(dirname(__file__), "../")
RESERVATION_URL = 'https://www.unimore.it/covid19/trovaaula.html'
TIME_INTERVAL = 5


def find_hours(root_element, start_hour, end_hour):
    links = root_element.find_elements_by_tag_name("a")

    available_hours = (
        tuple(link.text.split(" ")[2].split("-"))
        for link in links
    )

    def check_range(x):
        try:
            range_start = time(int(x[0].split(":")[0]), int(x[0].split(":")[1]))
            range_end = time(int(x[1].split(":")[0]), int(x[1].split(":")[1]))
        except (TypeError, ValueError):
            return False

        return (range_start <= start_hour < range_end) or (range_end >= end_hour > range_start)

    ranges_to_reserve = list(filter(
        check_range,
        available_hours
    ))

    print(ranges_to_reserve)

    return ranges_to_reserve


def reserve_room(driver, lesson):
    element = driver.find_element_by_xpath(
        f"//li[contains(text(), '{lesson.classroom.building.name}')]"
        "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
    )
    driver.execute_script("arguments[0].click();", element)

    room_element = driver.find_element_by_xpath(
        f"//td[contains(text(), '{lesson.classroom}')]/ancestor::tr"
    )

    ranges = find_hours(room_element, lesson.start_time, lesson.end_time)

    building_url = driver.current_url
    # TODO: sembra che questo ciclo faccia un'iterazione in più!
    for range_start_time, range_end_time in ranges:
        element = driver.find_element_by_xpath(
            f"//td[contains(text(), '{lesson.classroom}')]"
            f"/ancestor::tr//a[contains(text(), 'Turno Aula {range_start_time}-{range_end_time}')]"
        )
        driver.execute_script("arguments[0].click();", element)

        try:
            driver.find_element_by_id("username").send_keys(lesson.user.plain_unimore_username)
            driver.find_element_by_id("password").send_keys(lesson.user.plain_unimore_password)

            driver.find_element_by_name("_eventId_proceed").click()
        except NoSuchElementException:
            pass

        button = driver.find_element_by_xpath("//button[contains(text(), 'Inserisci')]")
        # button.click()
        Reservation.objects.create(link=driver.current_url, lesson=lesson)
        print(f"Presenza inserita {range_start_time}-{range_end_time}")

        driver.get(building_url)


def reserve_lesson_map(lesson):
    # Allows to run Firefox on a system with no display
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    # Selenium configuration:
    driver.implicitly_wait(TIME_INTERVAL)

    print(f'Reserving: {lesson}')
    """
    l'ideale è creare ad esempio 3 tab e ciclare iterativamente su di essi con l'operatore modulo, in questo modo
    dovremmo ottimizzare al massimo il driver e l'occupazione di memoria e cpu.

    ogni map calcola che tab utilizzare (mediante un contatore globale + operatore modulo(3)) e fa quello che deve 
    su quel tab.

    Il driver a quel punto viene creato direttamente dal main così può essere chiuso da lì.
    """
    # driver.execute_script(f"window.open('{RESERVATION_URL}', '_blank');")
    driver.get(RESERVATION_URL)
    reserve_room(driver, lesson)
    driver.delete_all_cookies()
    driver.close()


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings")
    django.setup()

    from reservation_management.models import Lesson, Reservation, Log

    # Delete old reservations
    Reservation.objects.all().delete()

    lessons = Lesson.objects.filter(
        day=datetime.now(pytz.timezone('Europe/Rome')).weekday(),
        user__enable_automatic_reservation=True
    )

    start = measure_time()
    # TODO: understand if this assignment is required...
    dummy_var = list(map(reserve_lesson_map, lessons))
    end = measure_time()

    Log.objects.create(
        execution_time=(start - end),
        users=len(set(lesson.user for lesson in lessons)),
        lessons=len(lessons),
    )
