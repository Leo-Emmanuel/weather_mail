import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_weather_email(to_email, weather_data):

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        raise ValueError("Gmail credentials are missing")

    weather = weather_data["weather"]

    message = EmailMessage()

    message["Subject"] = f"Weather Report - {weather_data['city']}"
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_email

    message.set_content(f"""
Hello,

Here is your requested weather report.

City: {weather_data['city']}
Country: {weather_data['country']}
Precipitation: {weather['precipitation']} mm
Temperature: {weather['temperature']} °C
Humidity: {weather['humidity']} %
Feels Like: {weather['feels_like']} °C
Wind Speed: {weather['wind_speed']} km/h

Thank you for using our Weather Report Application.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(message)

    return True
