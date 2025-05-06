import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        logging.info(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        logging.warning("Sorry, I could not understand your command.")
        return None
    except sr.RequestError:
        logging.error("Sorry, there was an error with the speech recognition service.")
        return None
