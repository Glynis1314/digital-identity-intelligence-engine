import time
import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def check_github(driver, username):

    # Profile URL
    url = f"https://github.com/{username}"

    # Open page
    driver.get(url)

    # Wait for loading
    time.sleep(3)

    # Default result
    result = {
        "platform": "GitHub",
        "username": username,
        "found": False,
        "profile_name": None,
        "bio": None,
        "url": url,
        "screenshot": None
    }

    # Check if profile exists
    if "Not Found" not in driver.page_source:

        result["found"] = True

        # Extract profile name
        try:
            name_element = driver.find_element(
                By.CLASS_NAME,
                "p-name"
            )

            result["profile_name"] = name_element.text

        except NoSuchElementException:
            result["profile_name"] = None

        # Extract bio
        try:
            bio_element = driver.find_element(
                By.CLASS_NAME,
                "p-note"
            )

            result["bio"] = bio_element.text

        except NoSuchElementException:
            result["bio"] = None

        # Create screenshots folder
        os.makedirs("screenshots", exist_ok=True)

        # Screenshot path
        screenshot_path = f"screenshots/{username}_github.png"

        # Save screenshot
        driver.save_screenshot(screenshot_path)

        result["screenshot"] = screenshot_path

    return result