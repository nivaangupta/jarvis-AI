import speech_recognition as sr
from gtts import gTTS
import playsound
import requests
import json

url = "http://localhost:11434/api/generate"
recognizer = sr.Recognizer()
headers = {
    'Content-Type': 'application/json',
}
data = {
    "model": "mistral",
    "prompt": "",
    "stream": False,}

def SpeakText(text_):
    speech = gTTS(text=text_, lang="en", slow=False, tld="com.au")
    speech.save("prompt.mp3")
    playsound.playsound("prompt.mp3")

def AudioToText():
    while (1):
        try:
            with sr.Microphone() as source2:
                recognizer.adjust_for_ambient_noise(source2, duration=0.2)
                print("I am Listening")
                audio2 = recognizer.listen(source2)
                MyAudioText = recognizer.recognize_google(audio2)
                print(MyAudioText)
                return MyAudioText
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("unkown error occured")

def TextToAi(data_):
    print("AI is working its magic")
    response = requests.post(url, headers=headers, data=json.dumps(data_))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        print(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)

while (1):
    text = AudioToText()
    data = {
    "model": "mistral",
    "prompt": text,
    "stream": False,}
    response = TextToAi(data)
    SpeakText(response)
    print(response)
