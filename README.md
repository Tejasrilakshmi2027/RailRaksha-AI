# 🚆 RailRaksha AI

## Smart Railway Safety, Security and Passenger Assistance Platform

RailRaksha AI is an AI-powered railway safety and passenger assistance system built for the **FAR AWAY 2026 Hackathon – Railways Theme**.  
The project helps railway staff monitor safety incidents, assist passengers, detect vehicle license plates, track officer actions, and generate incident reports from one simple dashboard.

---

## 📌 Problem Statement

Railway stations face several real-world challenges such as:

- Delayed emergency response
- Heavy crowding near platforms
- Lost luggage and passenger complaints
- Suspicious vehicles near station premises
- Manual monitoring workload for railway staff
- Lack of centralized incident tracking
- Difficulty in updating action status after an alert is reported

RailRaksha AI solves these problems by combining AI chatbot support, safety alert classification, license plate detection, and officer action tracking into one platform.

---

## ✅ Proposed Solution

RailRaksha AI provides a smart railway command system where:

- Passengers can ask railway-related queries through an AI assistant.
- Emergency and safety incidents are classified based on risk level.
- Vehicles near railway premises can be scanned using license plate detection.
- Officers can update action status as Pending, In Progress, or Resolved.
- Staff can view dashboards, graphs, logs, and reports.
- Incident reports can be downloaded for review and monitoring.

---

## 🌟 Key Features

### 🤖 AI Railway Passenger Assistant

The assistant helps passengers with:

- Emergency support
- Lost luggage reporting
- Medical help
- Crowd complaints
- Ticket and refund guidance
- Train/platform-related assistance

Important passenger complaints automatically generate alerts in the staff dashboard.

---

### 🚨 Safety Alert System

The alert system classifies incident reports into:

- **Critical**: Fire, bomb threat, weapon, attack, explosion, track danger
- **High**: Accident, injured passenger, suspicious bag, medical emergency
- **Medium**: Crowd, lost item, restricted area, suspicious person
- **Low**: General railway report or normal passenger issue

---

### 🚘 License Plate Detection

The Plate Scan module detects vehicle plate numbers from uploaded images.

It helps railway staff:

- Monitor vehicles near station parking
- Record vehicles in restricted zones
- Flag suspicious vehicles
- Store plate number, image path, status, and timestamp

---

### 🛠️ Officer Action Tracking

Officers can update each alert by entering:

- Alert ID
- Officer name
- Action taken
- Status: Pending / In Progress / Resolved

This helps track whether railway staff has responded to an incident.

---

### 📊 Staff Command Dashboard

The dashboard shows:

- Total alerts
- High/Critical risks
- Pending actions
- In-progress actions
- Resolved actions
- Vehicle records
- Passenger query logs
- Risk severity graphs
- Officer action status graphs
- Vehicle security status graphs

---

### 📄 Incident Report Generator

RailRaksha AI can generate a downloadable text report containing:

- Safety alerts
- Risk severity
- Officer name
- Action taken
- Alert status
- Vehicle records
- Passenger chatbot queries
- Created and updated timestamps

---

## 🧠 Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Computer Vision | OpenCV |
| OCR | EasyOCR |
| Data Handling | Pandas, NumPy |
| Report Generation | Python File Handling |
| Deployment | Streamlit Cloud / Render |
| Version Control | GitHub |

---

## 📁 Project Structure

```text
RailRaksha-AI/
│
├── app.py
├── database.py
├── chatbot.py
├── alert_system.py
├── plate_detector.py
├── report_generator.py
├── requirements.txt
├── README.md
│
├── uploads/
├── detected/
├── reports/
└── railraksha.db

Save this file as:

```text
README.md