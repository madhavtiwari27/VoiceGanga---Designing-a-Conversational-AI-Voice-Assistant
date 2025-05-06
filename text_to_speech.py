import pyttsx3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

engine = pyttsx3.init()

voices = engine.getProperty('voices')
zira_voice = None

for voice in voices:
    if "zira" in voice.name.lower():
        zira_voice = voice
        break

if zira_voice:
    engine.setProperty('voice', zira_voice.id)
    logging.info(f"Using voice: {zira_voice.name}")
else:
    logging.warning("Zira voice not found. Using default voice.")

engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()
