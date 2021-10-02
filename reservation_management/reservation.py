from os.path import dirname

import django
import os
import sys
# import time as t
from time import time as measure_time

from datetime import time

from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PROJECT_PATH = os.path.join(dirname(__file__), "../")
RESERVATION_URL = 'https://www.unimore.it/covid19/trovaaula.html'
TIME_INTERVAL = 5


def find_hours(root_element, start_hour, end_hour):
    links = root_element.find_elements_by_tag_name("a")
    available_hours = [
        tuple(link.text.split(" ")[2].split("-"))
        for link in links
    ]

    ranges_to_reserve = list(filter(
        lambda x: (
            range_start := time(int(x[0].split(":")[0]), int(x[0].split(":")[1])),
            range_end := time(int(x[1].split(":")[0]), int(x[1].split(":")[1])),
            (range_start <= start_hour <= range_end) or
            (range_end >= end_hour >= range_start)
        )[-1],
        available_hours
    ))
    # t.sleep(1)

    return ranges_to_reserve


def reserve_room(driver, user, start_time, end_time, building, room):
    # TODO: FIRST SOLUTION (WITH SLEEPS)
    # if driver.find_element_by_id("cookie-bar"):
    #     driver.find_element_by_xpath(
    #         "//*[@id='cookie-bar']//a[contains(text(), 'OK')]"
    #     ).click()
    #     t.sleep(1)

    # driver.find_element_by_xpath(
    #     f"//li[contains(text(), '{building}')]"
    #     "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
    # ).click()
    # t.sleep(1)
    # TODO: SECOND SOLUTION, MAYBE USEFUL FOR FUTURE TASKS, BUT NOT IN THIS CASE...
    # WebDriverWait(driver, TIME_INTERVAL).until(EC.visibility_of_element_located(
    #     (
    #         By.XPATH,
    #         f"//li[contains(text(), '{building}')]"
    #         "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
    #     )
    # )).click()
    # TODO: THIRD SOLUTION, IT WORKS WITHOUT THE FIRST IF, PERFORMANCE TEST NEEDED AGAINST THE FIRST SOLUTION
    element = driver.find_element_by_xpath(
        f"//li[contains(text(), '{building}')]"
        "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
    )
    driver.execute_script("arguments[0].click();", element)

    room_element = driver.find_element_by_xpath(
        f"//td[contains(text(), '{room}')]/ancestor::tr"
    )
    
    ranges = find_hours(room_element, start_time, end_time)
    
    building_url = driver.current_url
    for range_start_time, range_end_time in ranges:
        driver.find_element_by_xpath(
            f"//td[contains(text(), '{room}')]"
            f"/ancestor::tr//a[contains(text(), 'Turno Aula {range_start_time}-{range_end_time}')]"
        ).click()
        # t.sleep(1)

        try:
            driver.find_element_by_id("username").send_keys(user.unimore_username)
            driver.find_element_by_id("password").send_keys(user.unimore_password)

            driver.find_element_by_name("_eventId_proceed").click()
            # t.sleep(1)
        except NoSuchElementException:
            pass

        button = driver.find_element_by_xpath("//button[contains(text(), 'Inserisci')]")
        print(f"{button.text} presenza {range_start_time}-{range_end_time}")
        driver.get(building_url)
        # t.sleep(1)

        # button.click()


def automatic_reservation():
    driver = webdriver.Firefox()
    # Selenium configuration:
    driver.implicitly_wait(TIME_INTERVAL)
    #driver.maximize_window()

    start_time = measure_time()
    for user in get_user_model().objects.exclude(enable_automatic_reservation=False):
        print(f"UTENTE {user.username} -----------------------------------------------------------------------------")
        for lesson in user.today_lessons:
            print(
                f"Prenotando {lesson.classroom.building.name} {lesson.classroom.name} - "
                f"{lesson.start_time}/{lesson.end_time}"
            )
            driver.get(RESERVATION_URL)
            reserve_room(
                driver,
                user,
                lesson.start_time,
                lesson.end_time,
                lesson.classroom.building.name,
                lesson.classroom.name
            )

        driver.delete_all_cookies()

    driver.close()
    end_time = measure_time()
    print(f"Elapsed time: {end_time - start_time}")


def reserve_lesson_map(lesson):
    driver = webdriver.Firefox()
    # Selenium configuration:
    driver.implicitly_wait(TIME_INTERVAL)
    # driver.maximize_window()

    print(f'Prenotando: {lesson}')
    driver.get(RESERVATION_URL)
    reserve_room(
        driver,
        lesson.user,
        lesson.start_time,
        lesson.end_time,
        lesson.classroom.building.name,
        lesson.classroom.name
    )


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings")

    django.setup()

    # automatic_reservation()
    from reservation_management.models import Lesson

    lessons = Lesson.objects.filter(day=3).order_by('start_time')
    start = measure_time()
    # TODO: understand if this assignment is required...
    a = list(map(reserve_lesson_map, lessons))
    end = measure_time()
    print(f'{end - start}')
