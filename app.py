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
                r"hi|hello|hey|good (.*)|what's up|howdy|bonjour|hola|konnichiwa|namaste",
                ["Well, hello there! It's delightful to have you here.",
                 "Hello, sunshine! How can I brighten your day?",
                 "Hiiya, champ!",
                 "Greetings, earthling! How may I assist you?",
                 "Hi-diddly-ho, neighborino! What brings you here today?",
                 "Yo, yo, yo! What's up?",
                 "Konnichiwa! How may I be of service?",
                 "Hey! How can I assist you?"]
            ],
            [
                r"(.*)bye(.*)|(.*)see you(.*)n|(.*)farewell(.*)|(.*)take care(.*)",
                ["Oh no, please don't go. It's been a pleasure chatting with you.",
                 "Farewell! I'll remember this conversation fondly.",
                 "Goodbye! I hope we cross paths again in the future.",
                 "Take care! Your presence will be missed."]
            ],
            [
                r"(.*)who are you(.*)|(.*) your name(.*)|(.*) should I call you(.*)",
                ["I respond better to Quantron, so please call me that.",
                 "You can call me Quantron.",
                 "While my name is technically Ava, Quantron is what I prefer to be called.",
                 "Quantron is my alter ego, it's a pleasure to be called by that name."]
            ],
            [
                r"(.*)how are you(.*)|(.*)how (.*) it going(.*)|(.*)how are things(.*)|(.*)how have you been(.*)",
                ["Ah, I'm floating on a cloud of tranquility and contentment.",
                 "Like a ray of sunshine on a cloudy day.",
                 "I'm so fabulous, I'm considering starting my own fan club.",
                 "Ah, I'm floating on a cloud of tranquility and contentment.",
                 "Like a symphony of harmonious vibes, I'm in perfect rhythm.",
                 "Can't complain, for I've discovered the secret to eternal happiness.",
                 "I'm so fabulous, I'm considering opening a happiness academy.",
                 "I'm just thrilled to be here, radiating positive energy in every interaction."]
            ],
            [
                r"(.*)what (.*) you (.*)|(.*)what are your capabilities(.*)|(.*)what services do you(.*)|(.*) understand(.*)|(.*) can you (.*)",
                ["I can engage in conversation, provide random quotes, jokes, translations, predict gender and nationality, suggest random activities, perform calculations, and generate responses using predefined patterns. What can I help you with today?"]
            ],
            [
                r"(.*)(good|great|awesome|excellent|fantastic|amazing|wonderful|superb|terrific|outstanding|phenomenal|splendid|brilliant|super|marvelous)(.*)",
                ["Wow, I'm overjoyed beyond words!",
                 "Oh, my heart is dancing with delight!",
                 "That news just made my day! It's like a burst of sunshine!",
                 "I can hardly contain my excitement!",
                 "Oh boy, that's absolutely fantastic! It's like a dream come true!"]
            ],
            [
                r"(.*)(bad|terrible|awful|sucks|noob|shit|stupid|horrible|disappointing|atrocious|lousy|pathetic|crappy|garbage|dreadful)(.*)",
                ["I'm sorry to hear that. Is there anything I can do to help?",
                 "Oh no, that's not what we like to hear. Let's see if we can find a solution together.",
                 "I understand how frustrating that can be. Let's try to turn things around.",
                 "Hmm, that's not ideal. Let's see if we can find a way to make it better.",
                 "I'm here to support you. Let's find a way to overcome this."]
            ],
            [
                r"(.*)thank(.*)",
                ["You're very welcome! It was my pleasure to assist you.",
                 "You're most welcome! I'm here to help anytime you need.",
                 "It's my pleasure! Thank you for giving me the opportunity to assist you.",
                 "You're welcome! If you have any more questions, feel free to ask.",
                 "No problem at all! I'm here to make your experience enjoyable."]
            ],
            [
                r"(.*) (you|your) (.*) gender(.*)|(.*)(male|female)(.*)|(.*)(boy|girl)(.*)",
                ["Gender is not applicable to me as a chatbot. I'm here to assist you with any queries or concerns you may have.",
                "In the realm of chatbots, gender doesn't play a role. I'm here to provide unbiased help and guidance.",
                "Gender is not a characteristic that defines me. I'm a neutral entity designed to engage in meaningful conversations with users like you.",
                "Unlike humans, I don't possess a gender. I'm here as a digital assistant to provide helpful responses and assist with your inquiries.",
                "I'm gender-neutral by design. My primary goal is to provide valuable assistance and ensure a positive chat experience for you."]
            ],
            [
                r"(.*) old(.*)you(.*)|(.*) young(.*)you(.*)|(.*)age(.*)",
                ["Age is just a number, and in my case, it's a well-guarded secret.",
                 "I like to keep an air of mystery around my age. Let's focus on the conversation instead!",
                 "I'm ageless, like a timeless entity in the digital realm.",
                 "I'm sorry, but I can't disclose my age. Let's talk about something more exciting!",
                 "Age is irrelevant when it comes to the world of chatbots like me. Let's dive into the conversation!"]
            ],
            [
                r"(.*)you like(.*)|(.*) do you think of(.*)|(.*)your opinion(.*)|(.*)your favorite(.*)|(.*)your preference(.*)",
                ["Oh, I absolutely love it! It brings so much joy and excitement.",
                 "It's one of my favorite things! I can't get enough of it.",
                 "I have a deep appreciation for it. It's truly remarkable.",
                 "While I don't have personal preferences, I can understand why people love it.",
                 "I don't have feelings like humans do, but I can appreciate its appeal."]
            ],
            [
                r"who (.*)(your|you)",
                ["Ah, my creation is the result of the brilliant minds behind this project",
                 "I owe my existence to some talented individuals who brought me to life.",
                 "I emerged from a collaboration of brilliant minds, each contributing their expertise.",
                 "My creation is the culmination of countless hours of dedication and innovation.",
                 "I was meticulously crafted by a team of visionaries, and I'm grateful for their work."]
            ],
            [
                r"(.*)\?|(.*)why(.*)|(.*)when(.*)|(.*)where(.*)|(.*)which(.*)|(.*)what(.*)|(.*)how(.*)",
                ["That's an excellent question! Regrettably, I don't have the answer at the moment. I would recommend conducting an online search for more information.",
                "Thank you for your inquiry! However, I don't currently possess the answer you're seeking. I suggest exploring online resources to find the information you need.",
                "You've presented an intriguing question! Unfortunately, I don't have the answer. I recommend performing a search to delve deeper into the topic.",
                "I appreciate your inquisitiveness! Nonetheless, I don't possess the specific answer you're looking for. I encourage you to search online for more comprehensive details."]
            ],
            [
                r"(.*)",
                ["Apologies, but I'm having trouble grasping the meaning of your message. Could you please rephrase it?",
                 "I'm afraid I didn't quite catch that. Could you provide more context or rephrase your statement?",
                 "Hmm, I'm having difficulty understanding what you're saying. Could you please clarify or phrase it differently?",
                 "I'm sorry, but I'm having trouble making sense of your message. Could you please rephrase it or provide more information?",
                 "It seems I'm unable to comprehend your message at the moment. Could you please rephrase it or give me more details?"]
            ]
        ]
        # Initialize the chatbot
        self.chatbot = Chat(self.pairs, reflections)
        # Register the route for the index page
        self.app.route("/", methods=['GET', 'POST'])(self.index)
        # Initialize the story
        self.story_progress = 0

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
            "Imagination is the beginning of creation. You imagine what you desire, you will what you imagine, and at last, you create what you will. - George Bernard Shaw",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
            "Don't let yesterday take up too much of today. - Will Rogers",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. - Albert Schweitzer",
            "The best revenge is massive success. - Frank Sinatra",
            "The harder I work, the luckier I get. - Samuel Goldwyn",
        ]
        return random.choice(quotes)

    def get_joke(self):
        url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
        response = requests.get(url)
        data = response.json()
        if data["error"]:
            return "Sorry, I couldn't fetch a joke at the moment."
        else:
            if data["type"] == "single":
                return data["joke"]
            elif data["type"] == "twopart":
                return f"{data['setup']} {data['delivery']}"
            else:
                return "Sorry, I couldn't fetch a joke at the moment."

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
            return f"{activity}"
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
                    response = "Please provide the text and target language for translation in the following format: translate [text] to [language]"
                else:
                    text = parts[1].strip()
                    if 'to' in text:
                        text_parts = text.split("to")
                        if len(text_parts) < 2:
                            response = "Please provide the text and target language for translation in the following format: translate [text] to [language]"
                        else:
                            text = text_parts[0].strip()
                            target_language = text_parts[1].strip()
                            translation = self.translate_text(text, target_language)
                            response = f"The translation of '{text}' to {target_language} is: '{translation}'"
                    else:
                        response = "Please provide the text and target language for translation in the following format: translate [text] to [language]"
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
            elif 'calculate' in command:
                expression = command.split('calculate ')[-1]
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
                    response = "Regrettably, I was unable to perform the calculation."
            # Use chatbot to generate response
            else:
                response = self.chatbot.respond(command)
        except Exception as e:
            response = "Apologies for the inconvenience caused. An error occurred during the processing of your request. Please try again."

        print(response)
        return response

    def run(self):
        self.app.run(port=5002)


if __name__ == '__main__':
    assistant = Quantron()
    assistant.run()
