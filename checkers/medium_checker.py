import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_medium(driver, username):

    url = f"https://medium.com/@{username}"

    driver.get(url)

    time.sleep(3)

    result = {
        "platform": "Medium",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    if "404" not in driver.page_source.lower():

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

        os.makedirs(
            "screenshots",
            exist_ok=True
        )

        screenshot_path = (
            f"screenshots/"
            f"{username}_medium.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        result["screenshot"] = screenshot_path

    return result