import cv2
import easyocr
import os
import re
from datetime import datetime
from database import save_plate

reader = easyocr.Reader(["en"], gpu=False)

SUSPICIOUS_PLATES = {
    "DL1CA1234",
    "MH12AB5678",
    "KA03MK4321"
}


def clean_plate_text(text):
    text = text.upper()
    text = text.replace(" ", "").replace("-", "").replace(".", "")
    text = re.sub(r"[^A-Z0-9]", "", text)
    return text


def detect_plate(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return "Not Detected", None, "Normal"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray)

    possible_plates = []

    for result in results:
        text = clean_plate_text(result[1])
        confidence = result[2]

        if confidence > 0.25 and len(text) >= 6:
            possible_plates.append(text)

    plate_number = possible_plates[0] if possible_plates else "Not Detected"

    status = "Suspicious" if plate_number in SUSPICIOUS_PLATES else "Normal"

    os.makedirs("detected", exist_ok=True)

    output_path = f"detected/detected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(output_path, image)

    save_plate(plate_number, output_path, status)

    return plate_number, output_path, status