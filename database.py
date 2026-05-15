import sqlite3
import json
from datetime import datetime


# Connect database
conn = sqlite3.connect(
    "scan_history.db",
    check_same_thread=False
)

cursor = conn.cursor()


# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS scans (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    scan_time TEXT,

    results TEXT,

    pdf_path TEXT
)
""")

conn.commit()


# Save scan
def save_scan(email, results, pdf_path):

    scan_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    results_json = json.dumps(results)

    cursor.execute("""

    INSERT INTO scans (
        email,
        scan_time,
        results,
        pdf_path
    )

    VALUES (?, ?, ?, ?)

    """, (
        email,
        scan_time,
        results_json,
        pdf_path
    ))

    conn.commit()


# Get all scans
def get_all_scans():

    cursor.execute("""

    SELECT id, email, scan_time

    FROM scans

    ORDER BY id DESC

    """)

    return cursor.fetchall()

# Get full scan history
def get_scan_history():

    cursor.execute("""

    SELECT
        id,
        email,
        scan_time,
        results,
        pdf_path

    FROM scans

    ORDER BY id DESC

    """)

    return cursor.fetchall()