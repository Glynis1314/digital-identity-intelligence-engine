import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_codeforces(driver, username):

    # Profile URL
    url = f"https://codeforces.com/profile/{username}"

    # Open page
    driver.get(url)

    # Wait for page load
    time.sleep(3)

    # Default result
    result = {
        "platform": "Codeforces",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    # Profile existence check
    if "handle not found" not in driver.page_source.lower():

        result["found"] = True

        # Extract profile name
        try:

            name_element = driver.find_element(
                By.CLASS_NAME,
                "main-info"
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
            f"{username}_codeforces.png"
        )

        # Save screenshot
        driver.save_screenshot(
            screenshot_path
        )

        result["screenshot"] = (
            screenshot_path
        )

    return result