from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from webbot import Browser
from time import time as measure_time


LOGIN_URL = "https://in.unimore.it"
TIME_INTERVAL = 5


def check_unimore_credentials(username, password):
    CORRECT_URL = "https://in.unimore.it/intra/"
    start = measure_time()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.headless = True

    driver = webdriver.Chrome(executable_path="/usr/lib/chromium/chromedriver", options=options)
    driver.implicitly_wait(TIME_INTERVAL)

    driver.get(LOGIN_URL)

    end = measure_time()
    print(f'Elpased time (create driver): {end - start}')
    start = measure_time()
    try:
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)

        driver.find_element_by_name("_eventId_proceed").click()
    except NoSuchElementException:
        driver.delete_allk_cookies()
        driver.quit()
        return False
    end = measure_time()
    print(f'Elpased time (compile form): {end - start}')
    start = measure_time()
    test_url = driver.current_url
    end = measure_time()
    print(f'Elpased time (search for Exit): {end - start}')
    driver.delete_all_cookies()
    driver.quit()

    return check_strings_equality(CORRECT_URL, test_url)


def check_strings_equality(first, second):
    return len(first) == len(second) and hash(first) == hash(second) and first == second    


def webbot_check(username, passwd):
    CORRECT_URL = "https://in.unimore.it/intra/"
    start = measure_time()
    driver = Browser(showWindow=False)
    end = measure_time()
    print(f'Elpased time (create driver): {end - start}')

    driver.go_to(LOGIN_URL)
    driver.type(username, id="username")
    driver.type(passwd, id="password")
    driver.click(tag="button", classname="form-button")
    test_url = driver.get_current_url()
    driver.quit()

    return check_strings_equality(CORRECT_URL, test_url)

if __name__ == "__main__":
    start = measure_time()
    check_unimore_credentials("username", "password")
    # webbot_check("username", "password")
    end = measure_time()
    print(f'Elpased time: {end - start}')
