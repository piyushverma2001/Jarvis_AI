import speech_recognition as sr
import os
import datetime
import openai
import random
import logging
from config import apikey

logging.basicConfig(filename="jarvis.log", level=logging.INFO, format="%(asctime)s - %(message)s")

chatStr = ""

def chat(query):
    global chatStr
    try:
        openai.api_key = apikey
        chatStr += f"Piyush: {query}\nJarvis: "

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        reply = response["choices"][0]["text"].strip()
        say(reply)
        chatStr += f"{reply}\n"

        logging.info(f"User: {query}\nJarvis: {reply}")
        return reply
    except Exception as e:
        logging.error(f"Error in OpenAI API: {e}")
        say("Sorry, I'm having trouble connecting to the server.")
        return "Sorry, I'm having trouble connecting to the server."

def ai(prompt):
    try:
        openai.api_key = apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************\n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text += response["choices"][0]["text"]

        if not os.path.exists("OpenAI"):
            os.mkdir("OpenAI")

        filename = f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(filename, "w") as f:
            f.write(text)
        
        logging.info(f"Saved AI response for prompt: {prompt}")
    except Exception as e:
        logging.error(f"Error in AI processing: {e}")
        say("Sorry, I couldn't process your request.")

def say(text):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except ImportError:
        if os.name == 'posix':
            os.system(f'say "{text}"')
        else:
            logging.error("Speech synthesis failed, pyttsx3 or system 'say' not available.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            logging.error("Could not understand the audio")
            return "Sorry, I didn't catch that."
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {e}")
            return "Sorry, I'm having trouble recognizing speech."

if __name__ == '__main__':
    print('Welcome to Jarvis A.I.')
    say("Hello, I am Jarvis. How can I assist you?")
    
    while True:
        query = takeCommand().lower()
        
        if "time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M")
            say(f"The current time is {current_time}")

        elif "using artificial intelligence" in query:
            ai(query)

        elif "jarvis quit" in query:
            say("Goodbye!")
            exit()

        elif "reset chat" in query:
            global chatStr
            chatStr = ""
            say("Chat reset.")

        else:
            chat(query)