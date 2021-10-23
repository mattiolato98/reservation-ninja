from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

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
