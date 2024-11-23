import logging
import os
import requests  
from fastapi import BackgroundTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_message(message: str):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,  
    }

    try:
        response = requests.get(url, params=params, timeout=60.0) 
        response.raise_for_status()  # Raise error for bad status codes

        if response.status_code == 200:
            logger.info("Message sent to Telegram successfully.")
        else:
            logger.error(f"Failed to send message. Status code: {response.status_code}")

    except requests.Timeout:
        logger.error("Request to Telegram API timed out.")
        send_alert_message("⏳ Timeout Alert! ⏰")
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        send_alert_message("⚠️ Request Error! 🛠")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        send_alert_message(f"😕 Unexpected Error! 🔍")

# Function to send a critical alert message (for errors, timeouts, etc.)
def send_alert_message(message: str):
    """
    Sends a critical alert to Telegram chat.
    This is a helper function that is used by `send_telegram_message`
    to alert the system about failures, timeouts, etc.
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        # Use requests to send the alert message synchronously
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure the request was successful
    except requests.RequestException as e:
        logger.error(f"Failed to send alert message to Telegram: {e}")

# Function to be called in the background task (for non-blocking alerts)
def send_alert_in_background(background_tasks: BackgroundTasks, message: str):
    """
    Adds the alert to background tasks to be handled asynchronously.
    This avoids blocking the main request while sending an alert.
    """
    background_tasks.add_task(send_telegram_message, message)
