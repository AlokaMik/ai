import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------


ACCESS_TOKEN = "EAANQ36eEyCUBO4kcwbZB4vbNb6Kq4byZArZAxBevTyq1AQnP4IKDagrStgxzwfWiPoXpqxudreiFwe0ixWHD7KCBHpELJg8asRW4fyjagxTWBfE3JN4xjqTHuXSVQ2Loz3ij4w1qVPoYcPJzZBvWcnQ0LWDeZBiUBOwKPNUshMSP9p1ZCp4vfZBZA0XiiaCA0NBlWJ1MCO8byBxEcxVJi7oPd5xjlLYZD"

APP_ID="933346448558117"
APP_SECRET="0e44da32ba3ba632fbd7d8c414bfecd8"
RECIPIENT_WAID="+263788329462" # Your WhatsApp number with country code (e.g., +31612345678)
VERSION="v18.0"
PHONE_NUMBER_ID="226800450524691"


 
# --------------------------------------------------------------
# Send a template WhatsApp message
# --------------------------------------------------------------


def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function
response = send_whatsapp_message()
print(response.status_code)
print(response.json())

# --------------------------------------------------------------
# Send a custom text WhatsApp message
# --------------------------------------------------------------

# NOTE: First reply to the message from the user in WhatsApp!


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, this is a test message."
)

response = send_message(data)

# --------------------------------------------------------------
# Send a custom text WhatsApp message asynchronously
# --------------------------------------------------------------


# Does not work with Jupyter!
async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = "https://graph.facebook.com" + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, this is a test message."
)

loop = asyncio.get_event_loop()
loop.run_until_complete(send_message(data))
loop.close()
