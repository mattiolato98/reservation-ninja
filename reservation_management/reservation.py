import time as t
from datetime import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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
    print(ranges_to_reserve)
    t.sleep(100)

    return ranges_to_reserve


def reserve_room(driver, start_time, end_time, building, room):
    driver.get("https://www.unimore.it/covid19/trovaaula.html")

    if driver.find_element_by_id("cookie-bar"):
        driver.find_element_by_xpath(
            "//*[@id='cookie-bar']//a[contains(text(), 'OK')]"
        ).click()
        t.sleep(1)

    driver.find_element_by_xpath(
        f"//li[contains(text(), 'Edificio {building}')]"
        "//a[contains(text(), 'Elenco Aule con link per registrazione presenza')]"
    ).click()
    t.sleep(1)

    room_element = driver.find_element_by_xpath(
        f"//td[contains(text(), 'Aula {room}')]/ancestor::tr"
    )
    
    ranges = find_hours(room_element, start_time, end_time)
    
    building_url = driver.current_url
    for range_start_time, range_end_time in ranges:
        driver.find_element_by_xpath(
            f"//td[contains(text(), 'Aula {room}')]"
            f"/ancestor::tr//a[contains(text(), 'Turno Aula {range_start_time}-{range_end_time}')]"
        ).click()
        t.sleep(1)

        try:
            driver.find_element_by_id("username").send_keys("")
            driver.find_element_by_id("password").send_keys("")

            driver.find_element_by_name("_eventId_proceed").click()
            t.sleep(1)
        except NoSuchElementException:
            pass

        button = driver.find_element_by_xpath("//button[contains(text(), 'Inserisci')]")
        print(f"{button.text} presenza {range_start_time}-{range_end_time}")
        driver.get(building_url)
        t.sleep(1)

        # button.click()

        # driver.close()


if __name__ == "__main__":   
    lessons = [
        {
            "start_time": time(9),
            "end_time": time(12),
            "building": "Fisica",
            "room": "L1.2"
        },
    ]
    driver = webdriver.Firefox()

    for lesson in lessons:
        reserve_room(
            driver,
            lesson["start_time"], 
            lesson["end_time"],
            lesson["building"], 
            lesson["room"]
        )
