from database import save_chat, save_alert


def railway_bot_response(query):
    q = query.lower()

    if any(word in q for word in ["emergency", "danger", "attack", "fire", "accident", "injured", "medical"]):
        response = (
            "Emergency request detected. Please move to a safe area immediately. "
            "Railway staff/RPF assistance has been alerted in the system."
        )
        save_alert("Passenger Emergency", query, "High")

    elif any(word in q for word in ["lost", "bag", "luggage", "wallet", "phone"]):
        response = (
            "Lost item report recorded. Please share item details, last seen location, "
            "and contact the station master or RPF help desk."
        )
        save_alert("Lost Item Report", query, "Medium")

    elif any(word in q for word in ["crowd", "rush", "stampede", "overcrowd"]):
        response = (
            "Crowd-related safety concern recorded. Railway staff should inspect the mentioned area."
        )
        save_alert("Crowd Alert", query, "Medium")

    elif any(word in q for word in ["platform", "train", "timing", "arrival", "departure"]):
        response = (
            "For live train platform and timing details, please check the official railway display board "
            "or enquiry system. This assistant can help with safety and station support."
        )

    elif any(word in q for word in ["ticket", "refund", "pnr", "booking"]):
        response = (
            "For ticket, refund, or PNR-related issues, please use the official IRCTC portal "
            "or visit the railway reservation counter."
        )

    elif any(word in q for word in ["suspicious", "unattended", "unknown person"]):
        response = (
            "Suspicious activity report recorded. Please avoid touching unattended objects "
            "and inform nearby railway staff immediately."
        )
        save_alert("Suspicious Activity", query, "High")

    else:
        response = (
            "I can help with railway safety, emergency support, lost luggage, crowd reports, "
            "ticket guidance, train/platform help, and passenger assistance."
        )

    save_chat(query, response)
    return response