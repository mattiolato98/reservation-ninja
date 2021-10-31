import django
import os
import sys

from os.path import dirname
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from django.contrib.auth import get_user_model

PROJECT_PATH = os.path.join(dirname(__file__), "../../")
LOGIN_URL = "https://in.unimore.it"
TIME_INTERVAL = 5


def check_data(user):
    print("----------------------------------------------------------------------------------------------------------")

    # Allows to run Firefox on a system with no display
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(TIME_INTERVAL)

    driver.get(LOGIN_URL)

    try:
        driver.find_element_by_id("username").send_keys(user.plain_unimore_username)
        driver.find_element_by_id("password").send_keys(user.plain_unimore_password)

        driver.find_element_by_name("_eventId_proceed").click()
    except NoSuchElementException:
        print(f"--- ERROR DURING AUTHENTICATION OF {user.username}---")
        driver.delete_all_cookies()
        driver.quit()
        return user

    try:
        driver.find_element_by_xpath("//a[contains(text(), 'Esci')]").click()
        print(f"{user.username} OK")
    except NoSuchElementException:
        print(f"{user.username} wrong credentials")
        driver.delete_all_cookies()
        driver.quit()
        return user

    driver.delete_all_cookies()
    driver.quit()


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), PROJECT_PATH))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reservation_tool_base_folder.settings")
    django.setup()

    users = get_user_model().objects.filter(
        enable_automatic_reservation=True,
        credentials_ok=True,
    )

    wrong_users = list(set(map(check_data, users)))

    if len(wrong_users) > 0:
        for user in filter(lambda x: x is not None, wrong_users):
            print(user.email)
    else:
        print("ALL CREDENTIALS CORRECT")
