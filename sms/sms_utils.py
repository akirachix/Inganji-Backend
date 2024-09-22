import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms(phone_number, message):
    # if not validate_phone_number(phone_number):
    #     logger.error(f"Invalid phone number: {phone_number}")
    #     return None

    headers = {
        "Authorization": f"Basic {settings.SMSLEOPARD_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "source": "AkiraChix",
        "message": message,
        "destination": [{"number": phone_number}],
    }
    try:
        logger.info(f"Sending SMS with payload: {payload}")
        response = requests.post(
            settings.SMSLEOPARD_API_URL, json=payload, headers=headers
        )
        logger.info(f"Response received: {response.status_code} - {response.text}")
        response_data = response.json()
        if response.status_code == 201 and response_data.get("success"):
            logger.info(f"SMS sent successfully: {response_data}")
            return response_data
        else:
            logger.error(f"Failed to send SMS: {response_data}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        print(f"Sending SMS to {phone_number}: {message}")
# sms_utils.py
def validate_phone_number(phone_number):
    return phone_number.startswith('0') and phone_number.isdigit() and len(phone_number) == 10

