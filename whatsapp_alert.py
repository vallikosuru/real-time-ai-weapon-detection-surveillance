import os
from twilio.rest import Client
from datetime import datetime

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

FROM_WHATSAPP = os.getenv(
    "TWILIO_FROM_WHATSAPP",
    "whatsapp:+14155238886"
)

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_whatsapp_alert(to_number, message):
    """
    Sends a WhatsApp message using Twilio.
    """
    try:
        msg = client.messages.create(
            from_=FROM_WHATSAPP,
            to=f"whatsapp:{to_number}",
            body=message
        )
        return msg.sid

    except Exception as e:
        print("WhatsApp alert error:", e)
        return None


def weapon_detected_alert(
    client_number,
    camera_id,
    detected_objects,
    confidence_scores
):
    """
    Sends an alert when a potential weapon is detected.
    """

    if not detected_objects or not confidence_scores:
        print("No valid detections to send alert")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weapons_list = []

    for obj, conf in zip(detected_objects, confidence_scores):
        weapons_list.append(
            f"{obj} ({float(conf) * 100:.2f}%)"
        )

    weapons_text = ", ".join(weapons_list)

    message = f"""🚨 CRITICAL ALERT: POTENTIAL WEAPON DETECTED!

Location/ID: {camera_id}
Timestamp: {timestamp}
Detected Objects: {weapons_text}

Immediate attention required.
Status: Guard response pending.

Dashboard:
https://weapon-detection-system-2026.web.app
"""

    sid = send_whatsapp_alert(
        client_number,
        message.strip()
    )

    if sid:
        print("WhatsApp alert sent successfully.")
    else:
        print("Failed to send WhatsApp alert.")


if __name__ == "__main__":
    TEST_CLIENT_NUMBER = os.getenv("TEST_CLIENT_NUMBER")

    if TEST_CLIENT_NUMBER:
        weapon_detected_alert(
            client_number=TEST_CLIENT_NUMBER,
            camera_id="CAM-01 / IMAGE_SCAN",
            detected_objects=["Automatic Rifle"],
            confidence_scores=[0.9672]
        )
