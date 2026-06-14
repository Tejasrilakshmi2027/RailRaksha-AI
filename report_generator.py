from datetime import datetime
import os


def generate_incident_report(alerts, plates, chats):
    os.makedirs("reports", exist_ok=True)

    report_path = "reports/railraksha_incident_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("RailRaksha AI - Railway Safety Incident Report\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        total_alerts = len(alerts)
        total_plates = len(plates)
        total_chats = len(chats)

        critical_alerts = sum(1 for alert in alerts if len(alert) > 3 and alert[3] == "Critical")
        high_alerts = sum(1 for alert in alerts if len(alert) > 3 and alert[3] == "High")
        medium_alerts = sum(1 for alert in alerts if len(alert) > 3 and alert[3] == "Medium")
        low_alerts = sum(1 for alert in alerts if len(alert) > 3 and alert[3] == "Low")

        pending_alerts = sum(1 for alert in alerts if len(alert) > 4 and alert[4] == "Pending")
        in_progress_alerts = sum(1 for alert in alerts if len(alert) > 4 and alert[4] == "In Progress")
        resolved_alerts = sum(1 for alert in alerts if len(alert) > 4 and alert[4] == "Resolved")

        suspicious_vehicles = sum(1 for plate in plates if len(plate) > 3 and plate[3] == "Suspicious")
        normal_vehicles = sum(1 for plate in plates if len(plate) > 3 and plate[3] == "Normal")

        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total Safety Alerts        : {total_alerts}\n")
        f.write(f"Critical Alerts            : {critical_alerts}\n")
        f.write(f"High Risk Alerts           : {high_alerts}\n")
        f.write(f"Medium Risk Alerts         : {medium_alerts}\n")
        f.write(f"Low Risk Alerts            : {low_alerts}\n")
        f.write(f"Pending Actions            : {pending_alerts}\n")
        f.write(f"In Progress Actions        : {in_progress_alerts}\n")
        f.write(f"Resolved Actions           : {resolved_alerts}\n")
        f.write(f"Total Vehicle Records      : {total_plates}\n")
        f.write(f"Normal Vehicles            : {normal_vehicles}\n")
        f.write(f"Suspicious Vehicles        : {suspicious_vehicles}\n")
        f.write(f"Passenger Queries Handled  : {total_chats}\n\n")

        f.write("1. SAFETY ALERT DETAILS\n")
        f.write("=" * 70 + "\n\n")

        if alerts:
            for alert in alerts:
                alert_id = alert[0] if len(alert) > 0 else "N/A"
                alert_type = alert[1] if len(alert) > 1 else "N/A"
                message = alert[2] if len(alert) > 2 else "N/A"
                severity = alert[3] if len(alert) > 3 else "N/A"
                status = alert[4] if len(alert) > 4 else "Pending"
                officer_name = alert[5] if len(alert) > 5 else "Not Assigned"
                action_taken = alert[6] if len(alert) > 6 else "No action taken yet"
                created_time = alert[7] if len(alert) > 7 else "N/A"
                updated_time = alert[8] if len(alert) > 8 else "N/A"

                f.write(f"Alert ID        : {alert_id}\n")
                f.write(f"Alert Type      : {alert_type}\n")
                f.write(f"Message         : {message}\n")
                f.write(f"Severity        : {severity}\n")
                f.write(f"Status          : {status}\n")
                f.write(f"Officer Name    : {officer_name}\n")
                f.write(f"Action Taken    : {action_taken}\n")
                f.write(f"Created Time    : {created_time}\n")
                f.write(f"Updated Time    : {updated_time}\n")
                f.write("-" * 70 + "\n\n")
        else:
            f.write("No safety alerts recorded.\n\n")

        f.write("2. VEHICLE PLATE RECORDS\n")
        f.write("=" * 70 + "\n\n")

        if plates:
            for plate in plates:
                plate_id = plate[0] if len(plate) > 0 else "N/A"
                plate_number = plate[1] if len(plate) > 1 else "N/A"
                image_path = plate[2] if len(plate) > 2 else "N/A"
                vehicle_status = plate[3] if len(plate) > 3 else "Normal"
                timestamp = plate[4] if len(plate) > 4 else "N/A"

                f.write(f"Vehicle Record ID : {plate_id}\n")
                f.write(f"Plate Number      : {plate_number}\n")
                f.write(f"Image Path        : {image_path}\n")
                f.write(f"Vehicle Status    : {vehicle_status}\n")
                f.write(f"Timestamp         : {timestamp}\n")
                f.write("-" * 70 + "\n\n")
        else:
            f.write("No vehicle plate records found.\n\n")

        f.write("3. PASSENGER QUERY LOGS\n")
        f.write("=" * 70 + "\n\n")

        if chats:
            for chat in chats:
                chat_id = chat[0] if len(chat) > 0 else "N/A"
                user_query = chat[1] if len(chat) > 1 else "N/A"
                bot_response = chat[2] if len(chat) > 2 else "N/A"
                timestamp = chat[3] if len(chat) > 3 else "N/A"

                f.write(f"Chat ID         : {chat_id}\n")
                f.write(f"Passenger Query : {user_query}\n")
                f.write(f"Bot Response    : {bot_response}\n")
                f.write(f"Timestamp       : {timestamp}\n")
                f.write("-" * 70 + "\n\n")
        else:
            f.write("No passenger queries recorded.\n\n")

        f.write("4. SYSTEM NOTE\n")
        f.write("=" * 70 + "\n")
        f.write(
            "This report was generated automatically by RailRaksha AI. "
            "It summarizes railway safety alerts, officer actions, vehicle records, "
            "and passenger support interactions for monitoring and review.\n"
        )

    return report_path