import os
from twilio.rest import Client

# ----------------------------
# Twilio Configuration
# ----------------------------
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

FROM_WHATSAPP = os.getenv(
    "TWILIO_FROM_WHATSAPP",
    "whatsapp:+14155238886"
)

TO_WHATSAPP = os.getenv("TEST_CLIENT_NUMBER")

# ----------------------------
# Create Twilio Client
# ----------------------------
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ----------------------------
# WhatsApp Test Message
# ----------------------------
message = client.messages.create(
    from_=FROM_WHATSAPP,
    to=f"whatsapp:{TO_WHATSAPP}",
    body="🚨 Weapon Detection Alert!\n"
         "Test message from Surveillance AI system."
)

print("Message sent successfully!")
print("Message SID:", message.sid)
