from flask import Flask, request, jsonify
import pyttsx3
import speech_recognition as sr
import cv2
import os
import random
import pyjokes
import wikipedia
from time import sleep
import datetime

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from other devices
from flask_cors import CORS
CORS(app)

engine = pyttsx3.init('sapi5')
engine.setProperty("rate", 178)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Listening function
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
        except Exception as e:
            return "None"

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data.get('text', '')
    speak(text)
    return jsonify({"status": "success", "message": f"Spoken: {text}"})

@app.route('/wikipedia', methods=['POST'])
def search_wikipedia():
    data = request.json
    query = data.get('query', '')
    try:
        results = wikipedia.summary(query, sentences=2)
        return jsonify({"status": "success", "result": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/joke', methods=['GET'])
def tell_joke():
    joke = pyjokes.get_joke()
    return jsonify({"status": "success", "joke": joke})

@app.route('/time', methods=['GET'])
def report_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    return jsonify({"status": "success", "time": current_time})

# Add more endpoints as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
