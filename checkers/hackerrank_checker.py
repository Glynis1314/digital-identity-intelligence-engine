import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_hackerrank(driver, username):

    # Profile URL
    url = f"https://www.hackerrank.com/profile/{username}"

    # Open page
    driver.get(url)

    # Wait for loading
    time.sleep(3)

    # Default result
    result = {
        "platform": "HackerRank",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    # Basic existence check
    if "Page Not Found" not in driver.page_source:

        result["found"] = True

        # Extract profile name
        try:

            name_element = driver.find_element(
                By.TAG_NAME,
                "h1"
            )

            result["profile_name"] = (
                name_element.text
            )

        except NoSuchElementException:

            result["profile_name"] = None

        # Create screenshots folder
        os.makedirs(
            "screenshots",
            exist_ok=True
        )

        # Screenshot path
        screenshot_path = (
            f"screenshots/"
            f"{username}_hackerrank.png"
        )

        # Save screenshot
        driver.save_screenshot(
            screenshot_path
        )

        result["screenshot"] = (
            screenshot_path
        )

    return result