import streamlit as st
import pandas as pd
import os

from database import (
    init_db,
    migrate_db,
    get_alerts,
    get_plates,
    get_chats,
    update_alert_status
)
from chatbot import railway_bot_response
from plate_detector import detect_plate
from alert_system import classify_safety_text
from report_generator import generate_incident_report


init_db()
migrate_db()

os.makedirs("uploads", exist_ok=True)
os.makedirs("detected", exist_ok=True)
os.makedirs("reports", exist_ok=True)

st.set_page_config(
    page_title="RailRaksha AI",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #edf6ff 0%, #f7fbff 45%, #ffffff 100%);
    }

    header[data-testid="stHeader"] {
        background: rgba(255,255,255,0);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(120deg, #061A40, #073B4C, #0B666A);
        padding: 42px;
        border-radius: 30px;
        color: white;
        box-shadow: 0px 18px 45px rgba(6, 26, 64, 0.28);
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 950;
        margin-bottom: 10px;
        color: white !important;
        letter-spacing: -1px;
    }

    .hero-text {
        font-size: 19px;
        color: #e8f7ff !important;
        line-height: 1.7;
        max-width: 1150px;
        font-weight: 500;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 18px;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 9px 15px;
        border-radius: 999px;
        color: white !important;
        font-size: 14px;
        font-weight: 800;
    }

    .nav-container {
        background: white;
        padding: 15px;
        border-radius: 22px;
        box-shadow: 0px 10px 30px rgba(10, 35, 80, 0.11);
        margin-bottom: 28px;
        border: 1px solid #dfe9f6;
    }

    .stButton > button {
        background: linear-gradient(90deg, #061A40, #0B666A) !important;
        color: white !important;
        border: none !important;
        padding: 0.78rem 1.1rem !important;
        border-radius: 15px !important;
        font-weight: 850 !important;
        transition: 0.22s ease-in-out !important;
        box-shadow: 0px 8px 20px rgba(6, 26, 64, 0.16);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #0B666A, #061A40) !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0px 12px 26px rgba(6, 26, 64, 0.22);
    }

    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: white !important;
        font-weight: 850 !important;
    }

    .section-title {
        font-size: 34px;
        font-weight: 950;
        color: #061A40 !important;
        margin-top: 12px;
        margin-bottom: 18px;
        letter-spacing: -0.5px;
    }

    .sub-heading {
        font-size: 25px;
        font-weight: 900;
        color: #061A40 !important;
        margin-top: 28px;
        margin-bottom: 10px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #061A40 !important;
        font-weight: 900 !important;
    }

    p, li, label, span {
        color: #061A40;
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 22px;
        border: 1px solid #dfe9f6;
        box-shadow: 0px 10px 28px rgba(10, 35, 80, 0.08);
        min-height: 178px;
        margin-bottom: 15px;
    }

    .card-title {
        font-size: 22px;
        font-weight: 900;
        color: #061A40 !important;
        margin-bottom: 10px;
    }

    .card-text {
        font-size: 15.5px;
        color: #41536c !important;
        line-height: 1.68;
        font-weight: 500;
    }

    .success-box {
        background: #eafff4;
        border-left: 7px solid #12a865;
        padding: 18px;
        border-radius: 16px;
        color: #064d2e !important;
        font-weight: 750;
        margin-top: 14px;
    }

    .warning-box {
        background: #fff8e5;
        border-left: 7px solid #f4a100;
        padding: 18px;
        border-radius: 16px;
        color: #5c3a00 !important;
        font-weight: 750;
        margin-top: 14px;
    }

    .danger-box {
        background: #fff0f0;
        border-left: 7px solid #e63946;
        padding: 18px;
        border-radius: 16px;
        color: #7a1018 !important;
        font-weight: 750;
        margin-top: 14px;
    }

    .critical-box {
        background: #ffe5e5;
        border-left: 7px solid #b00020;
        padding: 18px;
        border-radius: 16px;
        color: #65000f !important;
        font-weight: 850;
        margin-top: 14px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 22px;
        border: 1px solid #dfe9f6;
        box-shadow: 0px 10px 28px rgba(10, 35, 80, 0.08);
    }

    div[data-testid="stMetricLabel"] {
        color: #061A40 !important;
        opacity: 1 !important;
        font-weight: 900 !important;
        font-size: 15px !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #061A40 !important;
        opacity: 1 !important;
        font-weight: 900 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #001f54 !important;
        font-weight: 950 !important;
        font-size: 34px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #061A40 !important;
        font-weight: 850 !important;
        font-size: 16px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #e63946 !important;
        font-weight: 950 !important;
    }

    div[data-testid="stCaptionContainer"] {
        color: #334155 !important;
        font-weight: 650 !important;
    }

    textarea, input, select {
        border-radius: 14px !important;
    }

    .footer {
        text-align: center;
        color: #64748b !important;
        font-size: 14px;
        padding-top: 34px;
        padding-bottom: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "Home"


st.markdown("""
<div class="hero-box">
    <div class="hero-title">🚆 RailRaksha AI</div>
    <div class="hero-text">
        Smart Railway Safety, Security and Passenger Assistance Platform using AI chatbot support,
        license plate scanning, emergency alerts, safety risk classification, officer action tracking,
        and an easy command dashboard.
    </div>
    <div class="hero-badge">Built for FAR AWAY 2026 | Railways Theme | Working Prototype</div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="nav-container">', unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(6)

with nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav2:
    if st.button("🤖 Assistant", use_container_width=True):
        st.session_state.page = "Assistant"

with nav3:
    if st.button("🚘 Plate Scan", use_container_width=True):
        st.session_state.page = "Plate Scan"

with nav4:
    if st.button("🚨 Alerts", use_container_width=True):
        st.session_state.page = "Alerts"

with nav5:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

with nav6:
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"

st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.page


if page == "Home":
    st.markdown('<div class="section-title">Smart Railway Safety Platform</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🤖 AI Railway Assistant</div>
            <div class="card-text">
                Helps passengers with emergency support, lost luggage, platform guidance,
                ticket support, crowd complaints, and railway safety queries.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🚘 License Plate Scan</div>
            <div class="card-text">
                Detects vehicle plate numbers near station parking, restricted zones, and railway premises
                for security monitoring.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">🚨 Safety Risk Engine</div>
            <div class="card-text">
                Classifies railway incidents into Critical, High, Medium, and Low risk levels
                so staff can respond faster.
            </div>
        </div>
        """, unsafe_allow_html=True)

    alerts = get_alerts()
    plates = get_plates()

    critical_high_count = sum(1 for a in alerts if a[3] in ["Critical", "High"])
    pending_count = sum(1 for a in alerts if a[4] == "Pending")

    st.markdown('<div class="sub-heading">Live System Overview</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("🚨 Total Alerts", len(alerts))

    with m2:
        st.metric("🔴 High / Critical Risks", critical_high_count)

    with m3:
        st.metric("🚘 Detected Vehicles", len(plates))

    with m4:
        st.metric("⏳ Pending Actions", pending_count)

    st.markdown('<div class="sub-heading">Emergency Quick Actions</div>', unsafe_allow_html=True)

    e1, e2, e3, e4 = st.columns(4)

    with e1:
        if st.button("🔥 Fire Emergency", use_container_width=True):
            classify_safety_text("Fire emergency reported at railway station")
            st.markdown('<div class="critical-box">Fire emergency alert sent to staff dashboard.</div>', unsafe_allow_html=True)

    with e2:
        if st.button("🧍 Passenger Injured", use_container_width=True):
            classify_safety_text("Passenger injured near platform")
            st.markdown('<div class="danger-box">Medical emergency alert sent to staff dashboard.</div>', unsafe_allow_html=True)

    with e3:
        if st.button("🎒 Suspicious Bag", use_container_width=True):
            classify_safety_text("Suspicious unattended bag found near platform")
            st.markdown('<div class="danger-box">Suspicious bag alert sent to staff dashboard.</div>', unsafe_allow_html=True)

    with e4:
        if st.button("👥 Heavy Crowd", use_container_width=True):
            classify_safety_text("Heavy crowd and rush near railway platform")
            st.markdown('<div class="warning-box">Crowd alert sent to staff dashboard.</div>', unsafe_allow_html=True)

    st.markdown("""
    <br>
    <div class="success-box">
        Demo Flow: Click emergency action → Ask passenger query → Upload vehicle image →
        Officer updates action → View graphs and report in dashboard.
    </div>
    """, unsafe_allow_html=True)


elif page == "Assistant":
    st.markdown('<div class="section-title">🤖 AI Railway Passenger Assistant</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        user_query = st.text_area(
            "Enter passenger query",
            placeholder="Example: I lost my luggage near platform 2 / I need medical help / There is danger near platform 3",
            height=170
        )

        if st.button("Ask Assistant", use_container_width=True):
            if user_query.strip():
                response = railway_bot_response(user_query)
                st.markdown(f'<div class="success-box">{response}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a query.")

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Try Demo Queries</div>
            <div class="card-text">
                • I lost my bag near platform 2<br>
                • I need medical help<br>
                • Suspicious bag found near platform 3<br>
                • There is heavy crowd near ticket counter<br>
                • I have a ticket refund issue
            </div>
        </div>
        """, unsafe_allow_html=True)


elif page == "Plate Scan":
    st.markdown('<div class="section-title">🚘 License Plate Detection</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.45, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload vehicle image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            image_path = os.path.join("uploads", uploaded_file.name)

            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.image(image_path, caption="Uploaded Vehicle Image", use_container_width=True)

            if st.button("Detect Number Plate", use_container_width=True):
                plate_number, output_path, status = detect_plate(image_path)

                if status == "Suspicious":
                    st.markdown(
                        f'<div class="danger-box">Suspicious Vehicle Detected<br>Plate Number: {plate_number}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="success-box">Plate Number Detected: {plate_number}<br>Vehicle Status: {status}</div>',
                        unsafe_allow_html=True
                    )

                if output_path:
                    st.image(output_path, caption="Processed Image", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Security Purpose</div>
            <div class="card-text">
                This module helps railway staff record vehicles entering parking areas,
                restricted zones, and station premises.
                <br><br>
                Plate number, status, and timestamp are stored in the dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)


elif page == "Alerts":
    st.markdown('<div class="section-title">🚨 Safety Alert System</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        report = st.text_area(
            "Enter incident report",
            placeholder="Example: Fire near platform 1 / passenger injured / suspicious bag found / heavy crowd near platform 3",
            height=180
        )

        if st.button("Analyze Safety Risk", use_container_width=True):
            if report.strip():
                severity, message = classify_safety_text(report)

                if severity == "Critical":
                    st.markdown(f'<div class="critical-box">Critical Risk Detected: {message}</div>', unsafe_allow_html=True)
                elif severity == "High":
                    st.markdown(f'<div class="danger-box">High Risk Detected: {message}</div>', unsafe_allow_html=True)
                elif severity == "Medium":
                    st.markdown(f'<div class="warning-box">Medium Risk Detected: {message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-box">Low Risk Detected: {message}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter an incident report.")

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Risk Levels</div>
            <div class="card-text">
                <b>Critical:</b> bomb, fire, weapon, attack, explosion<br><br>
                <b>High:</b> accident, injured, danger, suspicious bag<br><br>
                <b>Medium:</b> crowd, lost item, restricted area<br><br>
                <b>Low:</b> general railway report
            </div>
        </div>
        """, unsafe_allow_html=True)


elif page == "Dashboard":
    st.markdown('<div class="section-title">📊 Railway Staff Command Dashboard</div>', unsafe_allow_html=True)

    alerts = get_alerts()
    plates = get_plates()
    chats = get_chats()

    high_count = sum(1 for a in alerts if a[3] in ["High", "Critical"])
    pending_count = sum(1 for a in alerts if a[4] == "Pending")
    in_progress_count = sum(1 for a in alerts if a[4] == "In Progress")
    resolved_count = sum(1 for a in alerts if a[4] == "Resolved")

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric("🚨 Alerts", len(alerts))

    with m2:
        st.metric("🔴 High/Critical", high_count)

    with m3:
        st.metric("⏳ Pending", pending_count)

    with m4:
        st.metric("🛠️ In Progress", in_progress_count)

    with m5:
        st.metric("✅ Resolved", resolved_count)

    if high_count > 0:
        st.markdown("""
        <div class="danger-box">
            Immediate staff attention required: High or Critical railway safety risks are present.
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🚨 Safety Alerts", "🚘 Vehicle Records", "🤖 Passenger Queries", "📄 Reports"]
    )

    with tab1:
        st.markdown('<div class="sub-heading">🚨 Safety Alert Records</div>', unsafe_allow_html=True)
        st.caption("This table shows all railway safety incidents and officer actions.")

        if alerts:
            df_alerts = pd.DataFrame(
                alerts,
                columns=[
                    "ID",
                    "Alert Type",
                    "Message",
                    "Severity",
                    "Status",
                    "Officer Name",
                    "Action Taken",
                    "Created Time",
                    "Updated Time"
                ]
            )

            st.dataframe(df_alerts, use_container_width=True)

            st.markdown('<div class="sub-heading">🛠️ Officer Action Panel</div>', unsafe_allow_html=True)
            st.caption("Officer can assign themselves, write action taken, and update alert status.")

            c1, c2 = st.columns(2)

            with c1:
                selected_id = st.number_input("Enter Alert ID", min_value=1, step=1)
                officer_name = st.text_input("Officer Name", placeholder="Example: RPF Officer Ravi")

            with c2:
                new_status = st.selectbox("Select Action Status", ["Pending", "In Progress", "Resolved"])
                action_taken = st.text_area(
                    "Action Taken",
                    placeholder="Example: Officer reached platform 2 and verified the situation.",
                    height=95
                )

            if st.button("Save Officer Action", use_container_width=True):
                if officer_name.strip() and action_taken.strip():
                    update_alert_status(selected_id, new_status, officer_name, action_taken)
                    st.success("Officer action saved successfully. Refresh or reopen dashboard to view updated status.")
                else:
                    st.warning("Please enter officer name and action taken.")

            st.markdown('<div class="sub-heading">📌 Graph 1: Risk Severity Distribution</div>', unsafe_allow_html=True)
            st.caption("This graph shows how many railway incidents are Critical, High, Medium, or Low risk.")

            severity_order = ["Critical", "High", "Medium", "Low"]
            severity_data = df_alerts["Severity"].value_counts().reindex(severity_order, fill_value=0)

            severity_df = pd.DataFrame({
                "Risk Level": severity_data.index,
                "Number of Incidents": severity_data.values
            })

            st.bar_chart(severity_df, x="Risk Level", y="Number of Incidents", use_container_width=True)

            st.markdown('<div class="sub-heading">Risk Level Meaning</div>', unsafe_allow_html=True)
            st.markdown("""
            - **Critical:** Fire, bomb threat, weapon, attack, explosion, track danger.
            - **High:** Accident, injured passenger, suspicious bag, medical emergency.
            - **Medium:** Crowd, lost item, restricted area, suspicious person.
            - **Low:** General railway report or normal passenger issue.
            """)

            st.markdown('<div class="sub-heading">📌 Graph 2: Officer Action Status Distribution</div>', unsafe_allow_html=True)
            st.caption("This graph shows how many alerts are Pending, In Progress, or Resolved.")

            status_order = ["Pending", "In Progress", "Resolved"]
            status_data = df_alerts["Status"].value_counts().reindex(status_order, fill_value=0)

            status_df = pd.DataFrame({
                "Officer Action Status": status_data.index,
                "Number of Alerts": status_data.values
            })

            st.bar_chart(status_df, x="Officer Action Status", y="Number of Alerts", use_container_width=True)

            st.markdown('<div class="sub-heading">Status Meaning</div>', unsafe_allow_html=True)
            st.markdown("""
            - **Pending:** Officer has not taken action yet.
            - **In Progress:** Officer is currently handling the issue.
            - **Resolved:** Officer completed the action and closed the issue.
            """)

        else:
            st.info("No safety alerts recorded yet.")

    with tab2:
        st.markdown('<div class="sub-heading">🚘 Vehicle Plate Records</div>', unsafe_allow_html=True)

        if plates:
            df_plates = pd.DataFrame(
                plates,
                columns=["ID", "Plate Number", "Image Path", "Status", "Timestamp"]
            )

            st.dataframe(df_plates, use_container_width=True)

            vehicle_order = ["Normal", "Suspicious"]
            vehicle_data = df_plates["Status"].value_counts().reindex(vehicle_order, fill_value=0)

            vehicle_df = pd.DataFrame({
                "Vehicle Status": vehicle_data.index,
                "Number of Vehicles": vehicle_data.values
            })

            st.markdown('<div class="sub-heading">📌 Graph 3: Vehicle Security Status</div>', unsafe_allow_html=True)
            st.bar_chart(vehicle_df, x="Vehicle Status", y="Number of Vehicles", use_container_width=True)

        else:
            st.info("No vehicle plates detected yet.")

    with tab3:
        st.markdown('<div class="sub-heading">🤖 Passenger Query Logs</div>', unsafe_allow_html=True)

        if chats:
            df_chats = pd.DataFrame(
                chats,
                columns=["ID", "User Query", "Bot Response", "Timestamp"]
            )

            st.dataframe(df_chats, use_container_width=True)

            query_df = pd.DataFrame({
                "Category": ["Passenger Queries"],
                "Count": [len(chats)]
            })

            st.markdown('<div class="sub-heading">📌 Graph 4: Passenger Query Count</div>', unsafe_allow_html=True)
            st.bar_chart(query_df, x="Category", y="Count", use_container_width=True)

        else:
            st.info("No chatbot queries recorded yet.")

    with tab4:
        st.markdown('<div class="sub-heading">📄 Incident Report Generator</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">Report Includes</div>
            <div class="card-text">
                Safety alerts, severity, officer name, action taken, status, vehicle records,
                passenger queries, created time, and updated time.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate Incident Report", use_container_width=True):
            report_path = generate_incident_report(alerts, plates, chats)

            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Incident Report",
                    data=file,
                    file_name="railraksha_incident_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )


elif page == "About":
    st.markdown('<div class="section-title">ℹ️ About RailRaksha AI</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Problem Statement</div>
            <div class="card-text">
                Railway stations face safety and security challenges such as crowding,
                delayed emergency response, lost luggage, suspicious vehicles,
                restricted-area monitoring, and manual workload for railway staff.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Proposed Solution</div>
            <div class="card-text">
                RailRaksha AI combines passenger assistance, safety risk detection,
                license plate scanning, and officer action tracking into one easy-to-use platform.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">Technology Stack</div>
            <div class="card-text">
                Python, Streamlit, OpenCV, EasyOCR, SQLite, Pandas, Computer Vision,
                Rule-based NLP, and Dashboard Analytics.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
            <div class="card-title">Future Scope</div>
            <div class="card-text">
                CCTV-based crowd detection, real-time railway API integration,
                multilingual voice assistant, RPF alert integration,
                face blurring for privacy, and IoT-based station sensors.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
        Hackathon Impact: RailRaksha AI improves railway safety, supports faster staff response,
        reduces manual monitoring effort, and gives passengers an accessible emergency support system.
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="footer">
    RailRaksha AI - Smart Railway Safety and Assistance Platform
</div>
""", unsafe_allow_html=True)