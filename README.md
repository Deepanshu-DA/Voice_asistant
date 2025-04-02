# Personal Assistant

This is a Python-based voice assistant that can perform various tasks such as retrieving weather information, launching applications, setting reminders, sending emails, and playing music or videos.

## Features
- **Speech Recognition:** Listens to voice commands and processes them.
- **Text-to-Speech:** Converts responses into speech output.
- **Weather Information:** Retrieves current weather based on location.
- **Application Launcher:** Opens applications installed on the system.
- **Reminders:** Sets reminders based on user input.
- **Email Service:** Sends emails using a configured SMTP server.
- **Media Playback:** Searches for and plays music/videos from YouTube.

## **Installation**  

1. Clone the repository:  
   ```sh
   git clone https://github.com/Deepanshu-DA/Voice_asistant.git
   ```

2. Install dependencies:  
   ```sh
   pip install -r requirements.txt

### Requirements
Ensure you have the following installed:
- Python 3.7+
- Required Python libraries:
  ```sh
  speechrecognition pyttsx3 requests smtplib geocoder beautifulsoup4 opencv-python pyaudio psutil
  ```
  *Note:* You may need to install `pyaudio` manually depending on your OS. Use the appropriate package manager.

### Environment Variables
Before running the assistant, set the following environment variables:
- `WEATHER_API_KEY`: API key for OpenWeatherMap.
- `EMAIL_ADDRESS`: Your email address for sending emails.
- `EMAIL_PASSWORD`: Your email password (consider using app passwords for security).

## Usage
Run the script using:
```sh
python main.py
```
The assistant will start listening for commands. Some examples:
- **"What's the weather like?"** - Fetches current weather.
- **"Open Notepad"** - Opens the Notepad application.
- **"Set reminder"** - Asks for time and message.
- **"Play music"** - Searches YouTube and plays music.
- **"Send email"** - Prompts for recipient, subject, and body.
- **"Stop"** - Ends the assistant.

## Future Improvements
- Add support for additional platforms.
- Enhance AI with NLP for better command recognition.
- Implement more integrations with third-party services.

## License
This project is open-source and available under the MIT License.

