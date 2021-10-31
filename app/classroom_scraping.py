import django
import os
import sys

from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from os.path import dirname

PROJECT_PATH = os.path.join(dirname(__file__), "../../")
TIME_INTERVAL = 5


def scrape_classrooms(building, table):
    counter = 1
    while True:
        try:
            classroom_name = table.find_element_by_xpath(
                f"((//tr)[{counter}]//td)[3]"
            ).text

            if len(Classroom.objects.filter(name=classroom_name)) == 0:
                print(f"Creating classroom {classroom_name} ({building.name})")
                Classroom.objects.create(
                    name=classroom_name,
                    building=building,
                )

            counter += 1
        except NoSuchElementException:
            break


def scrape(driver):
    for building_name in Building.objects.values_list('name'):
        driver.get("https://www.unimore.it/covid19/trovaaula.html")
        print(f"----------------- {building_name[0]} -----------------")

        building_name = building_name[0]
        apostrophe_adjusted = building_name.split("'")[0]
        x = driver.find_element_by_xpath(
            f"//li[contains(text(), '{apostrophe_adjusted}')]"
            "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
        )
        driver.execute_script("arguments[0].click();", x)

        try:
            table = driver.find_element_by_xpath("//table[@class='tabella-responsiva']/tbody")
            building = Building.objects.get(name=building_name)

            scrape_classrooms(building, table)
        except (NoSuchElementException, ObjectDoesNotExist):
            pass


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings")
    django.setup()

    from reservation_management.models import Building, Classroom

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    # Selenium configuration:
    driver.implicitly_wait(TIME_INTERVAL)

    scrape(driver)

    driver.delete_all_cookies()
    driver.close()
