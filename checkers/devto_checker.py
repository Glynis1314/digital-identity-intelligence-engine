import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_devto(driver, username):

    url = f"https://dev.to/{username}"

    driver.get(url)

    time.sleep(3)

    result = {
        "platform": "Dev.to",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    if "not found" not in driver.page_source.lower():

        result["found"] = True

        try:

            name_element = driver.find_element(
                By.TAG_NAME,
                "h1"
            )

            result["profile_name"] = (
                name_element.text
            )

        except NoSuchElementException:
            pass

        try:

            bio_element = driver.find_element(
                By.CLASS_NAME,
                "crayons-user__summary"
            )

            result["bio"] = bio_element.text

        except NoSuchElementException:
            pass

        os.makedirs(
            "screenshots",
            exist_ok=True
        )

        screenshot_path = (
            f"screenshots/"
            f"{username}_devto.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        result["screenshot"] = screenshot_path

    return result