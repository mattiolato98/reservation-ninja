from numpy import less
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd


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


def get_lesson_metadata(lesson):
    from datetime import time

    classroom, hours = lesson.split()
    start_time = time(int(hours.split("-")[0]))
    end_time = time(int(hours.split("-")[1]))

    return [classroom, start_time, end_time, get_building_from_classroom(classroom)]


def get_day_schedule(day_idx):
    keys_list = ["classroom", "start_time", "end_time", "building"]
    day_schedule_df = pd.read_csv(CLASS_SCHEDULE_FILE)[day_idx]

    day_schedule = [dict(zip(keys_list, get_lesson_metadata(lesson))) 
                    for lesson in day_schedule_df]
    return day_schedule


if __name__ == "__main__":
    credentials = get_credentials(PASSWD_FILE)
    day_idx = str(datetime.today().weekday())

    get_day_schedule(day_idx)

    # driver = webdriver.Firefox()
    # driver.get(URL)


    # lab_m02 = next(filter(
    #     lambda x: x.text == "Aula L1.6",
    #     driver.find_elements_by_tag_name("td")
    # ))


    # if driver.find_element_by_id("cookie-bar"):
    #     cookie_bar = driver.find_element_by_id("cookie-bar")
    #     next(filter(
    #         lambda x: x.text == "OK",
    #         cookie_bar.find_elements_by_tag_name("a")
    #     )).click()

    # link = next(filter(
    #     lambda x: x.text == "Turno Aula 11:00-16:00",
    #     lab_m02.find_element_by_xpath("..").find_elements_by_tag_name("a")
    # ))
    # link.click()

    # driver.implicitly_wait(5)  # wait to fully load the web page

    # # TODO: put credentials in another file! 
    # driver.find_element_by_id("username").send_keys(credentials.get("username"))
    # driver.find_element_by_id("password").send_keys(credentials.get("password"))

    # driver.find_element_by_name("_eventId_proceed").click()

    # button = next(filter(
    #     lambda x: x.text == "Inserisci",
    #     driver.find_elements_by_tag_name("button")
    # ))
    # # button.click()

    # # driver.close()