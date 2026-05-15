import os
from concurrent.futures import ThreadPoolExecutor

from database import save_scan

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import (
    ChromeDriverManager
)

from extractors.username_extractor import (
    extract_usernames
)

from checkers.github_checker import (
    check_github
)

from checkers.reddit_checker import (
    check_reddit
)

from checkers.leetcode_checker import (
    check_leetcode
)

from checkers.hackerrank_checker import (
    check_hackerrank
)

from checkers.codeforces_checker import (
    check_codeforces
)

from checkers.devto_checker import (
    check_devto
)

from checkers.medium_checker import (
    check_medium
)

from checkers.gfg_checker import (
    check_gfg
)


from correlation.confidence_scorer import (
    calculate_confidence
)

from utils.report_generator import (
    generate_pdf_report
)

from utils.risk_classifier import (
    classify_risk
)


# =========================
# Create Browser Driver
# =========================

def create_driver():

    options = Options()

    # =========================
    # Stealth Options
    # =========================

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    options.add_argument(
        "--disable-infobars"
    )

    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )

    # =========================
    # Deployment Safe Options
    # =========================

    options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    options.add_argument(
        "--disable-dev-shm-usage"
    )

    options.add_argument(
        "--window-size=1920,1080"
    )

    # =========================
    # Auto Install ChromeDriver
    # =========================

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    # =========================
    # Hide Selenium Detection
    # =========================

    driver.execute_script("""

    Object.defineProperty(
        navigator,
        'webdriver',
        {
            get: () => undefined
        }
    )

    """)

    return driver


# =========================
# Scan Single Username
# =========================

def scan_username(email, username):

    driver = create_driver()

    results = []

    try:

        # =========================
        # Platform Scanners
        # =========================

        platform_results = [

            check_github(driver, username),

            check_reddit(driver, username),

            check_leetcode(driver, username),

            check_hackerrank(driver, username),

            check_codeforces(driver, username),

            check_devto(driver, username),

            check_medium(driver, username),

            check_gfg(driver, username),

            check_instagram(driver, username),

            check_twitter(driver, username)

        ]

        # =========================
        # Process Results
        # =========================

        for result in platform_results:

            confidence = calculate_confidence(

                email,

                result["username"],

                result["found"],

                result.get("profile_name"),

                result.get("bio")

            )

            # Add confidence score
            result["confidence"] = confidence

            # Add risk classification
            result["risk_level"] = classify_risk(
                confidence
            )

            results.append(result)

    finally:

        driver.quit()

    return results


# =========================
# Main Scanning Engine
# =========================

def run_scan(email, progress_callback=None):

    # Generate username candidates
    usernames = extract_usernames(email)

    all_results = []

    # =========================
    # Parallel Scanning
    # =========================

    with ThreadPoolExecutor(
        max_workers=3
    ) as executor:

        futures = []

        # Start scanning tasks
        for username in usernames:

            future = executor.submit(

                scan_username,

                email,

                username

            )

            futures.append(future)

        # =========================
        # Track Progress
        # =========================

        completed = 0

        total = len(futures)

        # Collect results
        for future in futures:

            results = future.result()

            all_results.extend(results)

            completed += 1

            progress = completed / total

            # Update UI progress
            if progress_callback:

                progress_callback(progress)

    # =========================
    # Generate PDF Report
    # =========================

    pdf_path = generate_pdf_report(

        all_results,

        "identity_scan"

    )

    # =========================
    # Save Scan History
    # =========================

    save_scan(

        email,

        all_results,

        pdf_path

    )

    return all_results, pdf_path