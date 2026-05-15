from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from extractors.username_extractor import extract_usernames

from checkers.github_checker import check_github
from checkers.reddit_checker import check_reddit
from checkers.leetcode_checker import check_leetcode

from correlation.confidence_scorer import calculate_confidence

from utils.report_generator import generate_pdf_report

# Input email
email = "john.smith123@gmail.com"

# Generate usernames
usernames = extract_usernames(email)

print("Generated Usernames:")
print(usernames)

# ChromeDriver path
driver_path = "drivers/chromedriver.exe"

# Start browser
# Chrome options
options = Options()

# Enable headless mode
options.add_argument("--headless")

# Optional improvements
options.add_argument("--window-size=1920,1080")

# Start browser
service = Service(driver_path)

driver = webdriver.Chrome(
    service=service,
    options=options
)

# Store all results
all_results = []

# Loop through usernames
for username in usernames:

    print(f"\nScanning username: {username}")

    # Run platform checks
    results = [
        check_github(driver, username),
        check_reddit(driver, username),
        check_leetcode(driver, username)
    ]

    # Add confidence score
    for result in results:

        confidence = calculate_confidence(
            email,
            result["username"],
            result["found"]
        )

        result["confidence"] = confidence

        all_results.append(result)

# Print results
print("\nFINAL RESULTS:\n")

for result in all_results:
    print(result)

# Generate PDF report
pdf_path = generate_pdf_report(all_results, "identity_scan")

print(f"\nPDF Report Generated: {pdf_path}")

# Close browser
driver.quit()