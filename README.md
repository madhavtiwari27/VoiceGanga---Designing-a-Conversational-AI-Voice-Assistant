# VoiceGanga: Designing a Conversational AI Voice Assistant

## Description

1. VoiceGanga is a Python-based interactive voice assistant leveraging Natural Language Processing and Speech Processing technologies. The system integrates the NLTK library for linguistic analysis, SpeechRecognition Library for transcribing spoken input, and Pyttsx3 library for synthesizing vocal responses. Its user interface is rendered using the Pygame library, featuring a dynamic visual representation centered around a vertical oval.

2. Upon initialization, VoiceGanga establishes a graphical window and initializes necessary modules for audio processing and text manipulation. It continuously listens for user speech input in a background thread. When a user query is detected, it is transcribed into text. This textual input is then processed by an external NLP pipeline, which interprets the user's intent.

3. Based on the processed intent, VoiceGanga generates a textual response. The transcribed user input and the chatbot's textual response are displayed in designated areas within the graphical user interface, with long responses automatically wrapped for readability.

4. The architecture of VoiceGanga is designed for modularity, allowing for future expansion of its NLP capabilities and the integration of more sophisticated dialogue management strategies. VoiceGanga serves as a demonstrative platform for multimodal human-computer interaction, combining auditory and visual feedback to enhance the user experience in voice-driven applications.


## Pre-requisites

- **TensorFlow**
  > pip install tensorflow

- **NLTK**
  > pip install nltk

- **Pygame**
  > pip install pygame

- **SpeechRecognition**
  > pip install speechrecognition

- **Pyttsx3**
  > pip install pyttsx3


## Project Interface

Following is the voice assitant's user interface:

![Screenshot 2025-05-04 161927](https://github.com/user-attachments/assets/2430adf6-3190-4d66-b87b-16427e2f859b)


## References

1. [Veton Kepuska and Gamal Bohouta, “Next-Generation of Virtual Personal Assistants”, 2018 IEEE 8th Annual CCWC, DOI:10.1109/CCWC.2018.8301638](https://ieeexplore.ieee.org/document/8301638)

2. [Subhash S, Prajwal N Srivatsa, Ullas A, Santhosh B and Siddhesh S, “Artificial Intelligence based Voice Assistant”, 2020 Fourth World Conference on Smart Trends in Systems, Security and Sustainability, DOI:10.1109/WorldS450073.2020.9210344](https://ieeexplore.ieee.org/document/9210344) 

3. [Pratyush Jha and Akashdeep Dash, “Voice Assistant using Python”, ResearchGate, DOI:10.1109/ICCR56254.2022.9995997](https://www.researchgate.net/publication/375696378_VOICE_ASSISTANT_USING_PYTHON)

4. [Pawan Goyal, “Natural Language Processing”, SWAYAM Portal](https://www.youtube.com/playlist?list=PLD9cMgsLUr5542VGOnACXHX-OXMaCGDRO)

5. [Snehan Kekre, “Transfer Learning for NLP with TensorFlow Hub”, Coursera](https://www.coursera.org/projects/transfer-learning-nlp-tensorflow-hub)

6. [Infosys Wingspan, “Explore Machine Learning using Python”, Infosys Springboard](https://infyspringboard.onwingspan.com/web/en/app/toc/lex_auth_012600400790749184237_shared/overview#iss=https:/infyspringboard.onwingspan.com/auth/realms/infyspringboard&iss=https:/infyspringboard.onwingspan.com/auth/realms/infyspringboard)


