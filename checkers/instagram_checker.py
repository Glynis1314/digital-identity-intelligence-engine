import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_instagram(driver, username):

    url = f"https://www.instagram.com/{username}/"

    driver.get(url)

    time.sleep(5)

    result = {
        "platform": "Instagram",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    page = driver.page_source.lower()

    # Basic existence check
    if (
        "sorry, this page isn't available"
        not in page
    ):

        result["found"] = True

        try:

            name_element = driver.find_element(
                By.TAG_NAME,
                "h2"
            )

            result["profile_name"] = (
                name_element.text
            )

        except NoSuchElementException:
            pass

        # Screenshot
        os.makedirs(
            "screenshots",
            exist_ok=True
        )

        screenshot_path = (
            f"screenshots/"
            f"{username}_instagram.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        result["screenshot"] = screenshot_path

    return result