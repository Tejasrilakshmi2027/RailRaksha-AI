from database import save_alert


def classify_safety_text(text):
    q = text.lower()

    critical_keywords = [
        "bomb",
        "fire",
        "weapon",
        "attack",
        "explosion",
        "terror",
        "person fell",
        "track crossing",
        "electric shock"
    ]

    high_keywords = [
        "accident",
        "injured",
        "medical emergency",
        "fight",
        "danger",
        "suspicious bag",
        "unattended bag"
    ]

    medium_keywords = [
        "crowd",
        "rush",
        "lost",
        "restricted area",
        "delay",
        "confusion",
        "unknown person",
        "vehicle parked"
    ]

    for word in critical_keywords:
        if word in q:
            save_alert("Critical Railway Risk", text, "Critical")
            return "Critical", "Critical threat detected. Immediate RPF/staff action required."

    for word in high_keywords:
        if word in q:
            save_alert("High Safety Risk", text, "High")
            return "High", "High-risk railway safety issue detected."

    for word in medium_keywords:
        if word in q:
            save_alert("Medium Safety Risk", text, "Medium")
            return "Medium", "Medium-risk issue detected. Staff verification recommended."

    save_alert("General Report", text, "Low")
    return "Low", "Low-risk/general railway report recorded."