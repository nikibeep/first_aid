from flask import Flask, render_template, request, send_file
import os
import json
import random
import nltk
nltk.download('punkt')
import speech_recognition as sr
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from google.cloud import texttospeech_v1

app = Flask("FirstAid")

# Set the path to your JSON key file
json_key_path = "prefab-wave-395613-26155198bb68.json"

# Set up Google Cloud Text-to-Speech client using the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key_path
client = texttospeech_v1.TextToSpeechClient()

# Load intents from intents.json
intents_file_path = 'intents.json'
with open(intents_file_path, 'r') as file:
    intents = json.load(file)

print("Loaded intents:", intents)

# Initialize stemmer
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def get_matching_tag(input_tokens):
    tag_keywords = [intent['tag'] for intent in intents['intents']]
    for token in input_tokens:
        for keyword in tag_keywords:
            if token.lower() in keyword.lower():
                return keyword
    return None

def text_to_speech(text, output_file):
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    voice_params = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_file}")

def generate_response(tag):
    for intent in intents['intents']:
        if intent['tag'].startswith(tag):
            responses = intent['responses']
            return random.choice(responses)
    return "Please be more specific."

# Initialize the recognizer
recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process_uploaded_audio', methods=['POST'])
def process_uploaded_audio():
    try:
        print("Received uploaded audio")
        audio_file = request.files['audio']

        # Clear the previous response.mp3 if it exists
        if os.path.exists('static/response.mp3'):
                os.remove('static/response.mp3')

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            print("Processing the uploaded audio...")

            try:
                input_text = recognizer.recognize_google(audio)
                print("You said:", input_text)

                preprocessed_input = preprocess_text(input_text)
                print("Preprocessed input:", preprocessed_input)

                matched_tag = get_matching_tag(preprocessed_input)
                if matched_tag:
                    response = generate_response(matched_tag)
                    print("Response:", response)

                    output_mp3_path = "static/response.mp3"  # Define the output path for the MP3 file

                    text_to_speech(response, output_mp3_path)  # Use the text_to_speech function
                    print("Output MP3 saved at:", output_mp3_path)
                else:
                    print("No matching tag found.")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

        return "Audio processing complete."

    except Exception as e:
        print("Error processing uploaded audio:", e)
        return "Error processing uploaded audio", 500

if __name__ == "__main__":
    app.run(debug=True)
