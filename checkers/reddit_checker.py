import time
import os


def check_reddit(driver, username):

    # Reddit profile URL
    url = f"https://www.reddit.com/user/{username}"

    # Open page
    driver.get(url)

    # Wait for loading
    time.sleep(3)

    # Default result
    result = {
        "platform": "Reddit",
        "username": username,
        "found": False,
        "url": url,
        "screenshot": None
    }

    # Check if profile exists
    if "Sorry, nobody on Reddit goes by that name" not in driver.page_source:

        result["found"] = True

        # Create screenshots folder
        os.makedirs("screenshots", exist_ok=True)

        # Screenshot filename
        screenshot_path = f"screenshots/{username}_reddit.png"

        # Save screenshot
        driver.save_screenshot(screenshot_path)

        # Store path
        result["screenshot"] = screenshot_path

    return result