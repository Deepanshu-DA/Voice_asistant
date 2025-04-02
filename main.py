import os
import speech_recognition as sr
import requests
import pyttsx3
import smtplib
import webbrowser
import geocoder
import threading
import psutil
import cv2
import time
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
from bs4 import BeautifulSoup

recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an issue with the service.")
        return None


class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_by_coords(self, lat, lon):
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.base_url, params=params).json()

        if response.get("main"):
            weather_desc = response["weather"][0]["description"]
            temperature = response["main"]["temp"]
            return f"Weather: {weather_desc}, Temperature: {temperature}°C"
        return "Could not retrieve weather data."


class Geolocation:
    def get_location(self):
        g = geocoder.ip("me")
        return g.latlng if g.ok else None


class AppLauncher:
    def open_application(self, app_name):
        try:
            if os.name == "nt":
                os.system(f"start {app_name}")
            elif os.uname().sysname == "Darwin":
                os.system(f"open -a {app_name}")
            else:
                os.system(f"xdg-open {app_name}")
            speak(f"Opening {app_name}.")
        except Exception as e:
            speak(f"Error opening application: {e}")


class Reminder:
    def set_reminder(self, time_str, message):
        reminder_time = datetime.strptime(time_str, "%H:%M").time()
        threading.Thread(target=self.check_reminder, args=(reminder_time, message)).start()

    def check_reminder(self, reminder_time, message):
        while True:
            now = datetime.now().time()
            if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                speak(f"Reminder: {message}")
                break
            time.sleep(30)


class EmailService:
    def send_email(self, recipient, subject, message):
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            speak("Email sent successfully!")
        except Exception as e:
            speak(f"Failed to send email: {e}")


class MediaPlayer:
    def play_music_video(self, song):
        query = song.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={query}"
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        video_ids = re.findall(r'watch\?v=(\S{11})', str(soup))
        if video_ids:
            webbrowser.open(f"https://www.youtube.com/watch?v={video_ids[0]}")
            speak(f"Playing {song}.")
        else:
            speak("No video found.")


def listen_for_commands():
    weather_api = WeatherAPI()
    app_launcher = AppLauncher()
    reminder = Reminder()
    media_player = MediaPlayer()
    geolocation = Geolocation()
    email_service = EmailService()

    while True:
        command = listen()
        if command:
            if "weather" in command:
                location = geolocation.get_location()
                if location:
                    weather_info = weather_api.get_weather_by_coords(*location)
                    speak(weather_info)
                else:
                    speak("Could not determine your location.")
            elif "open" in command:
                app_name = command.replace("open ", "").strip()
                app_launcher.open_application(app_name)
            elif "set reminder" in command:
                speak("What should I remind you about?")
                reminder_message = listen()
                speak("At what time? (Format: HH:MM)")
                reminder_time = listen()
                if reminder_message and reminder_time:
                    reminder.set_reminder(reminder_time, reminder_message)
            elif "play music" in command:
                speak("What song would you like to play?")
                song = listen()
                media_player.play_music_video(song)
            elif "send email" in command:
                speak("Please provide the recipient's email address.")
                to_email = listen()
                speak("What is the subject?")
                subject = listen()
                speak("What should I say in the email?")
                body = listen()
                if to_email and subject and body:
                    email_service.send_email(to_email, subject, body)
            elif "stop" in command:
                speak("Goodbye!")
                break
            else:
                speak("I didn't understand that command.")


if __name__ == "__main__":
    listen_for_commands()