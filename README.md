# RailRaksha-AI

RailRaksha-AI is an intelligent railway safety system that uses AI and computer vision to detect unauthorized vehicle access, monitor railway infrastructure, and send real-time alerts to authorized personnel.

## Features

- **License Plate Detection**: Detects and recognizes vehicle license plates
- **Chatbot**: AI-powered assistant for queries and support
- **Alert System**: Real-time notification system for safety incidents
- **Database Management**: Stores and manages railway alerts and incidents
- **Safety Classification**: ML model for classifying safety risks

## Project Structure

```
RailRaksha-AI/
├── app.py                 # Main Flask application
├── database.py           # Database connection and operations
├── chatbot.py            # Chatbot logic and NLP
├── plate_detector.py     # License plate detection
├── alert_system.py       # Alert management system
├── requirements.txt      # Project dependencies
├── data/                 # Data storage
│   └── rail_alerts.csv   # Alert history
├── uploads/              # User uploaded files
├── detected/             # Detected plates and images
└── model/                # Pre-trained models
    └── safety_classifier.pkl
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

## Usage

Access the web interface at `http://localhost:5000`

## License

Proprietary - RailRaksha Inc.
