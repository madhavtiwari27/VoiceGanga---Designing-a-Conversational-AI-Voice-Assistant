import wikipedia
import webbrowser
import nltk
import logging
import os
import tensorflow as tf
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

WIKIPEDIA_USER_AGENT = os.getenv('WIKIPEDIA_USER_AGENT', "VoiceGanga/2.0")

wikipedia.set_lang('en')
wikipedia.set_user_agent(WIKIPEDIA_USER_AGENT)

def download_nltk_resource(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        logging.info(f"[nltk_data] Downloading package '{resource}'...")
        nltk.download(resource, quiet=True)

download_nltk_resource('punkt')
download_nltk_resource('wordnet')

MODEL_FILE = "chatbot_model.h5"

def create_chatbot_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(batch_shape=(batch_size, None)),  
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size, activation='softmax') 
    ])
    return model

training_data = [
    ("hi", "Hello! How can I help you today?"),
    ("hello", "Hi there! What can I do for you?"),
    ("how are you", "I'm doing well, thank you!"),
    ("what is your name", "I'm Ganga, your assistant."),
    ("tell me a joke", "Why don't scientists trust atoms? Because they make up everything!"),
    ("what is the weather", "I can't provide real-time weather information, but I can search online for you."),
    ("who is Albert Einstein", "Albert Einstein was a theoretical physicist who developed the theory of relativity."),
    ("what is the capital of France", "The capital of France is Paris."),
    ("exit", "Goodbye! Have a great day."),
    ("quit", "See you later!")
]

tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=False)
tokenizer.fit_on_texts([text for pair in training_data for text in pair])
word_index = tokenizer.word_index
vocab_size = len(word_index) + 1

def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])[0]
    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=max_seq_length, padding='post')
    return padded_sequence

max_seq_length = max(len(text) for pair in training_data for text in pair) 

embedding_dim = 256
rnn_units = 1024
batch_size = 1  

model = create_chatbot_model(vocab_size, embedding_dim, rnn_units, batch_size)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy') 

epochs = 5
for epoch in range(epochs):
    logging.info(f"Epoch {epoch + 1}")
    for input_text, output_text in training_data:
        input_padded = preprocess_text(input_text)
        output_sequence = tokenizer.texts_to_sequences([output_text])[0]
        output_padded = tf.keras.preprocessing.sequence.pad_sequences([output_sequence], maxlen=max_seq_length, padding='post')

        model.layers[1].reset_states() 
        model.train_on_batch(input_padded, np.expand_dims(output_padded, -1))

def generate_chatbot_response(input_text):
    input_padded = preprocess_text(input_text)
    model.layers[1].reset_states() 
    predictions = model.predict(input_padded)
    predicted_ids = np.argmax(predictions[0], axis=-1)
    response_tokens = tokenizer.sequences_to_texts([predicted_ids])[0].split()

    valid_response = [token for token in response_tokens if token != 'pad']
    if valid_response:
        return " ".join(valid_response).strip()
    else:
        return "Sorry, I'm not sure how to respond to that."

def process_input(user_input):
    user_input_lower = user_input.lower()

    if "search" in user_input_lower or "find" in user_input_lower:
        query = user_input.replace("search", "").replace("find", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} on Google."

    if "who" in user_input_lower or "what" in user_input_lower or "where" in user_input_lower or "when" in user_input_lower:
        try:
            result = wikipedia.summary(user_input, sentences=3)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            if len(options) <= 5:
                return f"Sorry, there were multiple results. Please be more specific: {', '.join(options)}"
            else:
                return "Sorry, there were too many results. Please be more specific."
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information for that."
        except wikipedia.exceptions.HTTPTimeoutError:
            return "Sorry, there was a timeout error while fetching the data."
        except Exception as e:
            return f"Sorry, I couldn't retrieve information for that: {str(e)}"

    return generate_chatbot_response(user_input)
