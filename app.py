import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_scan_history
from scanner import run_scan

# Page config
st.set_page_config(
    page_title="Digital Identity Intelligence Engine",
    layout="wide"
)

# =========================
# Sidebar
# =========================

st.sidebar.title("Scan History")

history = get_scan_history()

if history:

    for scan in history:

        scan_id = scan[0]
        scan_email = scan[1]
        scan_time = scan[2]

        st.sidebar.markdown(f"""
        **{scan_email}**

        {scan_time}

        ---
        """)

else:

    st.sidebar.write("No previous scans.")

# =========================
# Custom Cyber Theme
# =========================

st.markdown("""
<style>

body {
    background-color: #0E1117;
    color: white;
}

.stApp {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #00FFAA;
}

div.stButton > button {
    background-color: #00FFAA;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #00CC88;
    color: white;
}

[data-testid="stTextInput"] input {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #00FFAA;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Title Section
# =========================

st.markdown("""
# Digital Identity Intelligence Engine

### Cyber Intelligence & Identity Correlation Dashboard
""")

# Description
st.write(
    "Analyze public digital identities using email correlation."
)

# =========================
# Email Input
# =========================

email = st.text_input(
    "Enter Email Address"
)

# =========================
# Scan Button
# =========================

if st.button("Start Scan"):

    if email.strip() == "":

        st.error("Please enter an email address.")

    else:

        # Progress UI
        progress_bar = st.progress(0)

        status_text = st.empty()

        # Progress callback
        def update_progress(value):

            progress_bar.progress(value)

            percentage = int(value * 100)

            status_text.text(
                f"Scanning in progress... {percentage}%"
            )

        # Run scan
        with st.spinner("Scanning identities..."):

            results, pdf_path = run_scan(
                email,
                progress_callback=update_progress
            )

        # Finish status
        status_text.text("Scan completed!")

        st.success("Scan Completed!")

        # =========================
        # Metrics
        # =========================

        total_profiles = len(results)

        found_profiles = len(
            [r for r in results if r["found"]]
        )

        high_confidence = len(
            [
                r for r in results
                if r.get("confidence", 0) >= 70
            ]
        )

        # Dashboard metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Profiles Scanned",
            total_profiles
        )

        col2.metric(
            "Profiles Found",
            found_profiles
        )

        col3.metric(
            "High Confidence Matches",
            high_confidence
        )

        # =========================
        # Analytics Dashboard
        # =========================

        st.subheader("Analytics Dashboard")

        # Convert results to DataFrame
        df = pd.DataFrame(results)

        # -------------------------
        # Risk Distribution
        # -------------------------

        risk_counts = (
            df["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Count"
        ]

        fig_risk = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            title="Exposure Risk Distribution"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # -------------------------
        # Platform Detection Count
        # -------------------------

        platform_counts = (
            df[df["found"] == True]
            ["platform"]
            .value_counts()
            .reset_index()
        )

        platform_counts.columns = [
            "Platform",
            "Count"
        ]

        fig_platform = px.bar(
            platform_counts,
            x="Platform",
            y="Count",
            title="Detected Profiles by Platform"
        )

        st.plotly_chart(
            fig_platform,
            use_container_width=True
        )

        # -------------------------
        # Confidence Distribution
        # -------------------------

        fig_confidence = px.histogram(
            df,
            x="confidence",
            nbins=10,
            title="Confidence Score Distribution"
        )

        st.plotly_chart(
            fig_confidence,
            use_container_width=True
        )

        # =========================
        # Search & Filtering
        # =========================

        st.subheader("Search & Filtering")

        # Platform filter
        platform_filter = st.selectbox(
            "Filter by Platform",
            ["ALL"] + list(df["platform"].unique())
        )

        # Risk filter
        risk_filter = st.selectbox(
            "Filter by Risk Level",
            ["ALL"] + list(df["risk_level"].unique())
        )

        # Username search
        search_query = st.text_input(
            "Search Username"
        )

        # Apply filters
        filtered_results = results

        # Platform filtering
        if platform_filter != "ALL":

            filtered_results = [
                r for r in filtered_results
                if r["platform"] == platform_filter
            ]

        # Risk filtering
        if risk_filter != "ALL":

            filtered_results = [
                r for r in filtered_results
                if r.get("risk_level") == risk_filter
            ]

        # Username search
        if search_query.strip() != "":

            filtered_results = [
                r for r in filtered_results
                if search_query.lower()
                in r["username"].lower()
            ]

        # =========================
        # Scan Results
        # =========================

        st.subheader("Scan Results")

        # Loop through filtered results
        for result in filtered_results:

            with st.container():

                st.markdown("---")

                # Platform
                st.subheader(result["platform"])

                # Status
                if result["found"]:
                    st.success("FOUND")
                else:
                    st.error("NOT FOUND")

                # Confidence
                confidence = result.get(
                    "confidence",
                    0
                )

                risk = result.get(
                    "risk_level",
                    "LOW"
                )

                st.write(
                    f"Confidence Score: {confidence}%"
                )

                # Risk badge
                if risk == "HIGH":

                    st.error(
                        f"Exposure Risk: {risk}"
                    )

                elif risk == "MEDIUM":

                    st.warning(
                        f"Exposure Risk: {risk}"
                    )

                else:

                    st.success(
                        f"Exposure Risk: {risk}"
                    )

                # Profile name
                if result.get("profile_name"):

                    st.write(
                        f"Profile Name: {result['profile_name']}"
                    )

                # Bio
                if result.get("bio"):

                    st.write(
                        f"Bio: {result['bio']}"
                    )

                # URL
                st.write(
                    f"URL: {result['url']}"
                )

                # Screenshot
                if result.get("screenshot"):

                    st.image(
                        result["screenshot"],
                        width=500
                    )

        # =========================
        # PDF Download
        # =========================

        st.success("PDF Report Generated!")

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name="identity_report.pdf",
                mime="application/pdf"
            )