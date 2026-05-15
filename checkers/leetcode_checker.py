import time
import os


def check_leetcode(driver, username):

    # LeetCode profile URL
    url = f"https://leetcode.com/{username}/"

    # Open page
    driver.get(url)

    # Wait for loading
    time.sleep(3)

    # Default result
    result = {
        "platform": "LeetCode",
        "username": username,
        "found": False,
        "url": url,
        "screenshot": None
    }

    # LeetCode invalid profile detection
    if "Page Not Found" not in driver.page_source:

        result["found"] = True

        # Create screenshots folder
        os.makedirs("screenshots", exist_ok=True)

        # Screenshot path
        screenshot_path = f"screenshots/{username}_leetcode.png"

        # Save screenshot
        driver.save_screenshot(screenshot_path)

        # Store path
        result["screenshot"] = screenshot_path

    return result