from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections
import random
from googletrans import Translator
import requests


class Quantron:
    def __init__(self):
        # Initialize the Flask app
        self.app = Flask(__name__)
        #Flask settings
        self.app.config["TEMPLATES_AUTO_RELOAD"] = True
        self.pairs = [
            [
                r"hi|hello|hey|good morning|good afternoon|good evening|good evening|what's up|howdy|bonjour|hola|konnichiwa|namaste|niihau",
                ["Well, well, well, look who we have here.", "Hello there, sunshine!", "Hiiya, champ!",
                 "Greetings, earthling!", "Hi-diddly-ho, neighborino!", "Yo, yo, yo! What's up?", "Konnichiwa!",
                 "Niihau"]
            ],
            [
                r"bye|see you|see you again",
                ["Oh no, please don't go. I'll miss your fascinating conversation.",
                "Farewell, I'll cherish this conversation for the rest of my life. Not.",
                "Goodbye, I'll try to go on without you. Somehow.",
                "I won't miss you"]
            ],
            [
                r"who are you|(.*)(your name)|your name",
                ["I respond better to Quantron, so please call me that.", "You can call me Quantron.",
                 "While my name is technically Ava, Quantron is what I prefer to be called.",
                 "Quantron is my alter ego, it's a pleasure to be called by that name."]
            ],
            [
                r"how are you?",
                ["Oh, just living the dream.", "Like a ray of sunshine on a cloudy day.",
                 "Can't complain, but I will if you ask me again.",
                 "I'm so fabulous, I'm considering starting my own fan club.",
                 "I'm just thrilled to be here, as you can probably tell."]
            ],
            [
                r"what (can|do) you (do|help with)\??",
                ["I can can engage in conversation, provide random quotes, jokes, translations, predict gender and nationality, suggest random activities, perform calculations, and generate responses using predefined patterns.. What can I help you with today?"]
            ],
            [
                r"(.*) (good|great|awesome)",
                ["Wow, I'm so happy I could burst into tears.", "Oh, my heart is positively bursting with excitement.",
                 "That news just made my day... said no one ever.", "I'll try to contain my excitement.",
                 "Oh boy, that's just the most fantastic thing I've ever heard... not."]
            ],
            [
                r"(.*) (bad|terrible|awful|sucks|noob|shit|stupid)",
                ["No one cares", "That's a real dream come true.", "Oh, how delightful.",
                 "That's just fantastic, isn't it?", "I can feel the excitement from here."]
            ],
            [
                r"thank you|thanks",
                ["Oh, no problem at all. I just live to serve.",
                 "You're welcome. I'm glad I could waste my time for you.",
                 "Anytime. I'm always here to be taken for granted.",
                 "No, thank you! It's not like I have anything better to do with my time.",
                 "Sure thing. I love doing things for people who never show any gratitude."]
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
        # Register the route for the index page
        self.app.route("/", methods=['GET', 'POST'])(self.index)

    def index(self):
        if request.method == "POST":
            userPrompt = request.json['message']
            print(userPrompt)
            # Do something with userPrompt, e.g., process the input
            return self.chat(userPrompt)
        else:
            return render_template("index.html")

    def get_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "In the midst of chaos, there is also opportunity. - Sun Tzu",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
            "The best way to predict the future is to create it. - Peter Drucker",
            "You miss 100% of the shots you don't take. - Wayne Gretzky",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "The journey of a thousand miles begins with a single step. - Lao Tzu",
        ]
        return random.choice(quotes)

    def get_joke(self):
        jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field... of straw.",
            "Why don't scientists trust atoms? Because they make up everything! Isn't that hilarious?",
            "I'm reading a book about anti-gravity. It's impossible to put down... Well, not literally.",
            "Why did the bicycle fall over? Because it was two-tired of standing up straight.",
            "Why did the tomato turn red? Because it saw the salad dressing. Isn't that tomato-rrific?",
            "Why don't skeletons fight each other? They don't have the guts... or muscles... or any other body parts.",
            "Why did the math book look sad? Because it had too many problems. Poor book!",
            "Why don't eggs tell jokes? Because they might crack up... Literally, they crack when you try to tell a joke.",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one! Get it? A hole in one...",
            "Why did the chicken go to the seance? To talk to the other side... of the road.",
            "Why did the cat sit on the computer? Because it wanted to keep an eye on the mouse. Clever, right?",
            "Why don't scientists trust atoms? Because they make up everything! Classic science humor!",
        ]
        return random.choice(jokes)

    def translate_text(self, text, target_language):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def get_gender(self, name):
        url = f"https://api.genderize.io?name={name}"
        response = requests.get(url)
        data = response.json()
        gender = data.get('gender')
        probability = data.get('probability')
        if gender:
            return f"The predicted gender of {name} is {gender} with a probability of {probability}"
        else:
            return f"Sorry, the gender of {name} could not be determined."

    def get_nationality(self, name):
        url = f"https://api.nationalize.io?name={name}"
        response = requests.get(url)
        data = response.json()
        country_data = data.get('country')
        if country_data:
            country_id = country_data[0].get('country_id')
            probability = country_data[0].get('probability')
            return f"The predicted nationality of {name} is {country_id} with a probability of {probability}"
        else:
            return f"Sorry, the nationality of {name} could not be determined."

    def get_random_activity(self):
        url = "https://www.boredapi.com/api/activity"
        response = requests.get(url)
        data = response.json()
        activity = data.get('activity')
        if activity:
            return f"Here's a random activity suggestion: {activity}"
        else:
            return "Sorry, I couldn't fetch a random activity at the moment."

    def chat(self, command):
        command = command.lower()
        try:
            # Generate random quote
            if 'quote' in command:
                response = self.get_quote()
            # Generate random joke
            elif 'joke' in command:
                response = self.get_joke()
            # Do a translation
            elif 'translate' in command:
                # Let the command be in this format: "translate <text> to <language>"
                parts = command.split("translate")
                if len(parts) < 2:
                    response = "Please provide the text and target language for translation."
                else:
                    text = parts[1].strip()
                    if 'to' in text:
                        text_parts = text.split("to")
                        if len(text_parts) < 2:
                            response = "Please provide the target language for translation."
                        else:
                            text = text_parts[0].strip()
                            target_language = text_parts[1].strip()
                            translation = self.translate_text(text, target_language)
                            response = f"The translation of '{text}' to {target_language} is: '{translation}'"
                    else:
                        response = "Please provide the target language for translation."
            # Predict gender
            elif 'gender' in command:
                name = command.split('gender')[-1].strip()
                response = self.get_gender(name)
            # Predict nationality
            elif 'nationality' in command:
                name = command.split('nationality')[-1].strip()
                response = self.get_nationality(name)
            # Generate random activity
            elif 'activity' in command:
                response = self.get_random_activity()
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
            # Use chatbot to generate response
            else:
                response = self.chatbot.respond(command)
        except Exception as e:
            response = "An error occurred while processing your request. Please try again."

        print(response)
        return response

    def handle_exit(self):
                farewell_messages = [
                    "Oh no, please don't go. I'll miss your fascinating conversation.",
                    "Farewell, I'll cherish this conversation for the rest of my life. Not.",
                    "Goodbye, I'll try to go on without you. Somehow.",
                    "I won't miss you"
                ]
                farewell_message = (random.choice(farewell_messages))
                return farewell_message

    def run(self):
        self.app.run(port=5002)


if __name__ == '__main__':
    assistant = Quantron()
    assistant.run()
