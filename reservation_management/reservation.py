from os.path import dirname

import django
import os
import sys
from time import time as measure_time
from datetime import datetime
from datetime import time

import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

PROJECT_PATH = os.path.join(dirname(__file__), "../")
RESERVATION_URL = "https://www.unimore.it/covid19/trovaaula.html"
TIME_INTERVAL = 5


def find_hours(root_element, start_hour, end_hour):
    """
    This function find the available time range for the given classroom.

    Args:
        root_element (WebElement): element that represent the classroom.
        start_hour (time): starting hour.
        end_hour (time): ending hour.

    Returns:
        list: list containing the ranges to reserve.
    """
    links = root_element.find_elements_by_tag_name("a")

    available_hours = (tuple(link.text.split(" ")[2].split("-")) for link in links)

    def check_range(x):
        try:
            range_start = time(int(x[0].split(":")[0]), int(x[0].split(":")[1]))
            range_end = time(int(x[1].split(":")[0]), int(x[1].split(":")[1]))
        except (TypeError, ValueError):
            return False

        return (range_start <= start_hour < range_end) or (
            range_end >= end_hour > range_start
        )

    ranges_to_reserve = list(filter(check_range, available_hours))

    print(ranges_to_reserve)

    return ranges_to_reserve


def check_reservation_exist(begin_time, end_time, lesson):
    """
    This function actually check if a lesson is included in already created reservation.
    This happens, for example, when at least two lessons are contiguous in the same classroom.

    Args:
        begin_time (TimeField): reservation starting time.
        end_time (TimeField): reservation ending time.
        lesson (Lesson): lesson to reserve.

    Returns:
        UrlField: if another reservation was created before.
        Boolean (False): if no other reservations were created.
    """
    reservations = Reservation.objects.filter(
        lesson__user=lesson.user,
        lesson__classroom=lesson.classroom,
        start_time=begin_time,
        end_time=end_time,
    )
    return reservations[0].link if reservations else False


def reserve_room(driver, lesson):
    """
    This function actually reserves the given lesson through the Selenium
    web driver. The webdriver actually simulate an authentic browser instance.

    Args:
        - driver selenium.webdriver: Selenium Web Driver.
        - lesson (lesson): lesson to reserve.
    """
    element = driver.find_element_by_xpath(
        f'//li[contains(text(), "{lesson.classroom.building.name}")]'
        '//a[contains(text(), "Elenco Aule con link per registrazione presenza")]'
    )
    driver.execute_script("arguments[0].click();", element)

    room_element = driver.find_element_by_xpath(
        f"//td[contains(text(), '{lesson.classroom}')]/ancestor::tr"
    )

    # getting the time range available for the current lesson's classroom:
    ranges = find_hours(room_element, lesson.start_time, lesson.end_time)

    building_url = driver.current_url
    for range_begin_time, range_end_time in ranges:
        # in the case if multiple lessons are grouped in the same classroom and in the same
        # time window, the older reservation link is provided to the new one:
        if link := check_reservation_exist(range_begin_time, range_end_time, lesson):
            Reservation.objects.create(
                link=link,
                lesson=lesson,
                start_time=range_begin_time,
                end_time=range_end_time,
            )
            print(f"Presenza duplicata inserita {range_begin_time}-{range_end_time}")
        else:
            element = driver.find_element_by_xpath(
                f"//td[contains(text(), '{lesson.classroom}')]"
                f"/ancestor::tr//a[contains(text(), 'Turno Aula {range_begin_time}-{range_end_time}')]"
            )
            driver.execute_script("arguments[0].click();", element)

            try:
                driver.find_element_by_id("username").send_keys(
                    lesson.user.plain_unimore_username
                )
                driver.find_element_by_id("password").send_keys(
                    lesson.user.plain_unimore_password
                )

                driver.find_element_by_name("_eventId_proceed").click()
                print("Credentials passed correctly.")
            except NoSuchElementException:
                print("User already logged in.")

            try:
                button_xpath = "//button[contains(text(), 'Inserisci')]"
                WebDriverWait(driver, 10).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, button_xpath)
                    )
                ).click()
                Reservation.objects.create(
                    link=driver.current_url,
                    lesson=lesson,
                    start_time=range_begin_time,
                    end_time=range_end_time,
                )
                print(f"Presenza inserita {range_begin_time}-{range_end_time}")
            except NoSuchElementException:
                print(f"WRONG CREDENTIALS for user {lesson.user.username}")
                break
            except TimeoutException:
                print(f"ALREADY RESERVED by user {lesson.user.username}")

            driver.get(building_url)


def reserve_lessons(lesson):
    """
    This function is called by the map function for each lesson element in the
    map's iterable. It plans the reservation procedure.

    Args:
        - lesson reservation_management.models.Lesson: lesson that have to be reserved.
    """
    print(
        "----------------------------------------------------------------------------------------------------------"
    )
    print(f"Reserving: {lesson}")
    """
    l'ideale è creare ad esempio 3 tab e ciclare iterativamente su di essi con l'operatore modulo, in questo modo
    dovremmo ottimizzare al massimo il driver e l'occupazione di memoria e cpu.

    ogni map calcola che tab utilizzare (mediante un contatore globale + operatore modulo(3)) e fa quello che deve 
    su quel tab.

    Il driver a quel punto viene creato direttamente dal main così può essere chiuso da lì.
    """
    # Allows running Firefox on a system with no display
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    # Selenium configuration:
    driver.implicitly_wait(TIME_INTERVAL)

    driver.get(RESERVATION_URL)
    reserve_room(driver, lesson)
    driver.quit()


def get_webdriver():
    # Allows running Firefox on a system with no display
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox(
        executable_path=GeckoDriverManager().install(), options=options
    )
    driver.implicitly_wait(TIME_INTERVAL)  # Selenium configuration
    return driver


def main():
    # In the case the scheduler execute this script more than one time:
    if Log.objects.filter(
            date=datetime.now(pytz.timezone("Europe/Rome")).date()
    ).exists():
        sys.exit(0)

    # Delete old reservations
    Reservation.objects.all().delete()

    driver = get_webdriver()

    lessons = Lesson.get_today_lessons()

    begin = measure_time()
    for i, lesson in enumerate(lessons):
        driver.get(RESERVATION_URL)
        print("----------------------------------------------------------------------")
        print(f"Reserving: {lesson}")
        if i < len(lessons) - 1:
            # start new instance if the next user is different from the current one:
            if lesson.user != lessons[i + 1].user:
                driver.quit()
                driver = get_webdriver()

    driver.quit()
    end = measure_time()

    users = list(set(lesson.user for lesson in lessons))
    for user in users:
        user.feedback = False
        user.save()

    # print(f"END, time: {end - begin}")
    Log.objects.create(
        execution_time=(end - begin),
        users=len(users),
        lessons=len(lessons),
    )


if __name__ == "__main__":
    # Django environment initialization:
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings"
    )
    django.setup()

    from reservation_management.models import Lesson, Reservation
    from analytics_management.models import Log

    main()
