from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from webbot import Browser


LOGIN_URL = "https://in.unimore.it"
TIME_INTERVAL = 5


def check_unimore_credentials(username, password):
    # Allows to run Firefox on a system with no display
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(TIME_INTERVAL)

    driver.get(LOGIN_URL)

    try:
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)

        driver.find_element_by_name("_eventId_proceed").click()
    except NoSuchElementException:
        driver.delete_all_cookies()
        driver.quit()
        return False
    try:
        driver.find_element_by_xpath("//a[contains(text(), 'Esci')]").click()
    except NoSuchElementException:
        driver.delete_all_cookies()
        driver.quit()
        return False
    driver.delete_all_cookies()
    driver.quit()

    return True


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

