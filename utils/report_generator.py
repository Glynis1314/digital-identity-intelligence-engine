from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_pdf_report(results, username):

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # PDF path
    pdf_path = f"reports/{username}_report.pdf"

    # Create canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Digital Identity Intelligence Report")

    # Metadata
    c.setFont("Helvetica", 12)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.drawString(50, 720, f"Generated At: {timestamp}")
    c.drawString(50, 700, f"Target: {username}")

    # Starting position
    y = 650

    # Loop through results
    for result in results:

        platform = result["platform"]
        status = "FOUND" if result["found"] else "NOT FOUND"
        url = result["url"]
        screenshot = result["screenshot"]
        confidence = result.get("confidence", 0)

        profile_name = result.get("profile_name")
        bio = result.get("bio")

        # Platform
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{platform} -> {status}")

        y -= 20

        # Confidence
        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Confidence Score: {confidence}%")

        y -= 20

        # Profile Name
        if profile_name:

            c.drawString(
                70,
                y,
                f"Profile Name: {profile_name}"
            )

            y -= 20

        # Bio
        if bio:

            c.drawString(
                70,
                y,
                f"Bio: {bio}"
            )

            y -= 20

        # URL
        c.drawString(70, y, f"URL: {url}")

        y -= 20

        # Screenshot
        if screenshot and os.path.exists(screenshot):

            c.drawImage(
                screenshot,
                70,
                y - 120,
                width=250,
                height=120
            )

            y -= 140

        # Spacing
        y -= 30

        # Prevent overflow
        if y < 150:
            c.showPage()
            y = 750

    # Save PDF
    c.save()

    return pdf_path