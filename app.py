import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
from nltk.chat.util import Chat, reflections
import sys
import random
from flask import Flask, render_template


class AIAssistant:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        self.pairs = [
            [
                r"hi|hello|hey|good morning|good afternoon|good evening|good evening|what's up|howdy|bonjour|hola|konnichiwa|namaste|niihau",
                ["Well, well, well, look who we have here.", "Hello there, sunshine!", "Hiiya, champ!", "Greetings, earthling!", "Hi-diddly-ho, neighborino!", "Yo, yo, yo! What's up?", "Konnichiwa!", "Niihau"]
            ],
            [
                r"who are you|(.*)(your name)|your name",
                ["I respond better to Quantron, so please call me that.", "You can call me Quantron.", "While my name is technically Ava, Quantron is what I prefer to be called.", "Quantron is my alter ego, it's a pleasure to be called by that name."]
            ],
            [
                r"how are you?",
                ["Oh, just living the dream.", "Like a ray of sunshine on a cloudy day.", "Can't complain, but I will if you ask me again.", "I'm so fabulous, I'm considering starting my own fan club.", "I'm just thrilled to be here, as you can probably tell."]
            ],
            [
                r"what (can|do) you (do|help with)\??",
                ["I can help you with various tasks such as searching the web, checking the weather, setting reminders, and more. What can I help you with today?"]
            ],
            [
                r"(.*) (good|great|awesome)",
                ["Wow, I'm so happy I could burst into tears.", "Oh, my heart is positively bursting with excitement.", "That news just made my day... said no one ever.", "I'll try to contain my excitement.", "Oh boy, that's just the most fantastic thing I've ever heard... not."]
            ],
            [
                r"(.*) (bad|terrible|awful|sucks|noob|shit|stupid)",
                ["No one cares", "That's a real dream come true.", "Oh, how delightful.", "That's just fantastic, isn't it?", "I can feel the excitement from here."]
            ],
            [
                r"thank you|thanks",
                ["Oh, no problem at all. I just live to serve.", "You're welcome. I'm glad I could waste my time for you.", "Anytime. I'm always here to be taken for granted.", "No, thank you! It's not like I have anything better to do with my time.", "Sure thing. I love doing things for people who never show any gratitude."]
            ],
            [
                r"how old are you",
                ["None of you business", "I'm too shy to answer that question", "No thanks, I cannot disclose my age"]
            ],
            [
                r"do you like (.*)|you like(.*)",
                ["Oh, I absolutely love it. It's my favorite thing in the world.",
                 "It's just okay, I guess. I mean, it's not like I have any strong feelings about it or anything.",
                 "No, I hate it with a passion. Why do you ask?",
                 "Of course I love it. It's just the most amazing thing ever."]
            ],
            [
                r"who created you|who made you",
                ["Oh, just some mysterious and enigmatic fella who prefers to remain nameless. You know how it is."]
            ],
            [
                r"(.*)",
                ["I'm sorry, I didn't quite understand what you meant. Could you please rephrase yourself?",
                 "I'm not sure what you're asking. Can you please provide more context?"]
            ]
        ]
        # Initialize the chatbot
        self.chatbot = Chat(self.pairs, reflections)

    def speak(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def speech_to_text(self):
        r = sr.Recognizer()
        text = ""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            print("Processing...")
            text = r.recognize_google(audio)
            print("You said:", text)  # Print the recognized text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand you.")
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing the speech recognition service.")
        except KeyboardInterrupt:
            print("Speech recognition interrupted.")

        return text

    def get_time(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        response = 'The current time is %s' % now
        return response

    def chat(self, command):
        # Check if the user wants to exit
        if command.lower() == "bye":
            return "bye"
        try:
            # Check current time
            if 'time' in command:
                response = self.get_time()
            # Check the weather
            elif 'weather' in command:
                webbrowser.open('https://www.google.com/search?q=weather')
                response = 'Here is what I found for weather'
            # Search the web
            elif "search" in command:
                search_term = command.split("search")[-1]
                webbrowser.open('https://www.google.com/search?q=' + search_term)
                response = 'Here is what I found for ' + search_term
            # Open a specific website
            elif 'open' in command:
                website = command.split('open ')[-1]
                if website == 'YouTube':
                    webbrowser.open('https://www.youtube.com/')
                    response = 'Opening YouTube...'
                elif website == 'Google':
                    webbrowser.open('https://www.google.com/')
                    response = 'Opening Google...'
                else:
                    response = f'Sorry, I don\'t know how to open {website}.'
            # Make a calculation
            elif 'what is' in command:
                expression = command.split('what is ')[-1]
                expression = expression.replace('plus', '+')
                expression = expression.replace('minus', '-')
                expression = expression.replace('times', '*')
                expression = expression.replace('divided by', '/')
                expression = expression.replace('multiplied by', '*')
                expression = expression.replace('x', '*')
                try:
                    result = eval(expression)
                    response = f"The answer is {result}"
                except Exception as e:
                    response = "Sorry, I couldn't calculate that."
            # Play music
            elif 'play' in command and 'music' in command:
                genre = command.split('play')[-1].strip()
                webbrowser.open('https://www.youtube.com/results?search_query=' + genre)
                response = "Playing" + genre
            # Use chatbot to generate response
            else:
                response = self.chatbot.respond(command)
        except Exception as e:
            print("I'm sorry, I didn't quite understand what you meant. Could you please rephrase your question?")
            print(f"Error: {str(e)}")
            return "continue"  # Indicate that the conversation should continue

        print(response)
        self.engine.say(response)
        self.engine.runAndWait()
        return "continue"

    def start(self):
        print("How would you like to interact? (speak/type): ")
        input_method = input().lower()

        if input_method == "speak":
            self.chat_with_speaking()
        elif input_method == "type":
            self.chat_with_typing()
        else:
            print("Invalid input. Please try again.")
            self.start()

    def handle_conversation(self, input_function):
        while True:
            command = input_function("You: ")
            if command.lower() == "bye":
                self.handle_exit()
                break
            result = self.chat(command)
            if result == "start_over":
                self.handle_exit(start_over_prompt=False)
                break

    def chat_with_speaking(self):
        self.handle_conversation(lambda prompt: self.speech_to_text())

    def chat_with_typing(self):
        self.handle_conversation(input)

    def handle_exit(self, start_over_prompt=True):
        if start_over_prompt:
            restart = input("Would you like to start over? (yes/no): ")
            if restart.lower() == "yes":
                self.start()
            else:
                farewell_messages = [
                    "Oh no, please don't go. I'll miss your fascinating conversation.",
                    "Farewell, I'll cherish this conversation for the rest of my life. Not.",
                    "Goodbye, I'll try to go on without you. Somehow.",
                    "I won't miss you"
                ]
                print(random.choice(farewell_messages))
                sys.exit()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.start()
    app.run()
