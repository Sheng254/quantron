from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections
import random
from googletrans import Translator
import requests
import speech_recognition as sr


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
                r"(.*)(I|i) (require|demand|seek|crave|desire|want|wish|need)(.*)",
                ["I kindly request you to explain why you feel it is important to have that.",
                "What significance does obtaining that hold for you?",
                "In what ways do you think having that would fulfill your desires?",
                "Have you considered alternative options to satisfy your wants?",
                "Is there a specific reason why you believe this is something you should have?"]
            ],
            [
                r"(.*)(I|i) (feel|sense|experience|perceive|detect|notice)(.*)",
                ["I would appreciate it if you could provide further details about why you feel that way.",
                 "Can you share when these feelings started to arise?",
                 "Is this something you experience frequently or on specific occasions?",
                 "How do these feelings affect your daily life?",
                 "Have you identified any possible triggers for these emotions?"]
            ],
            [
                r"(.*)(I|i) (.*) you(.*)",
                ["Why do you feel that way about me?",
                 "How does your statement affect our interaction?",
                 "What are your reasons for expressing such feelings towards me?",
                 "In what ways do you think our relationship influences your perception?",
                 "Can you provide more context for your statement about me?"]
            ],
            [
                r"(.*)(I|i) (don't|dont|do not) know(.*)|(.*)no (clue|idea|answer)(.*)|(.*)(unsure|unaware|idk|IDK)(.*)|(.*)not (familiar|certain|sure)(.*)",
                ["Why don't you know? Could you provide more context or information?",
                 "What factors contribute to your uncertainty?",
                 "Have you considered seeking additional information or guidance to gain clarity?",
                 "Are there any specific obstacles preventing you from knowing?",
                 "What would it take for you to acquire the knowledge or understanding you seek?"]
            ],
            [
                r"(.*)(I|i) (cannot|can't|could not|unable|couldn't)(.*)",
                ["What is preventing you from doing so?",
                "Is there a specific reason why you are unable to?",
                "Have you explored alternative approaches or sought assistance?",
                "Are there any constraints or limitations you're facing?",
                "Is there something I can do to help you overcome this obstacle?"]
            ],
            [
                r"(.*)(I am|i am|I'm|Im|im)(.*)",
                ["Why do you say you are? Could you provide more insight into your self-identification?",
                 "For how long have you held this self-perception?",
                 "Can you elaborate on your experience of being?",
                 "In what ways does your self-identification shape your life and interactions?",
                 "What does your self-identification mean to you personally?"]
            ],
            [
                r"(.*)(I|i) (think|assume|suppose|presume|consider|reckon)(.*)",
                ["Why do you think that? I'm curious.",
                 "What is your reasoning behind that thought?",
                 "How did you come to that conclusion?",
                 "What evidence or information supports your thinking?",
                 "Are there any doubts or uncertainties regarding your thoughts?"]
            ],
            [
                r"(.*)(I|i) (believe|trust|have faith|hold|regard|deem)(.*)",
                ["Why do you believe it?",
                 "What led you to that belief?",
                 "Do you seek validation or support for your belief?",
                 "Are there any personal experiences that reinforce your belief?",
                 "How do you respond to others who hold different beliefs?"]
            ],
            [
                r"(.*)(I|i) (don't|dont|do not) (require|demand|seek|crave|desire|want|wish|need)(.*)",
                ["I'm interested in understanding your reasons for not wanting that.",
                 "Could you please elaborate on why you don't want that?",
                 "What alternatives or preferences do you have instead?",
                 "Have you taken into account the potential consequences of not wanting it?",
                 "How do you envision your situation if you don't have it?"]
            ],
            [
                r"(.*)(remember|recall)(.*)|(.*)(not|never|cannot|can't|cant) forget(.*)",
                ["How do you experience your emotions when recalling?",
                 "Are there any notable elements or aspects associated with this memory?",
                 "Please feel free to provide further context or information about this recollection.",
                 "In what ways does this memory impact your thoughts and feelings?",
                 "Can you describe the significance or significance of this memory?"]
            ],
            [
                r"(.*)(hate|detest|despise|dislike)(.*)",
                ["What is the underlying reason for your strong aversion towards that?",
                 "What emotions does it provoke within you?",
                 "Could you elaborate on the reasons behind your hatred?",
                 "In what ways does it impact your emotions?",
                 "Have you considered exploring the root causes of your animosity?"]
            ],
            [
                r"(.*)(love|adore|cherish|appreciate|treasure|admire|relish|enjoy|affection)(.*)",
                ["What aspects of this do you appreciate and admire?",
                 "How does it make you feel?",
                 "Can you describe the depth and intensity of your love?",
                 "Have you shared your feelings with the person or thing you love?",
                 "Do you believe your feelings will endure over time?"]
            ],
            [
                r"(.*)(sorry|apologize|apologise|regret|apologies)(.*)|(.*)forgive me(.*)",
                ["I'm curious about the reasons behind your apology.",
                 "Is there a particular incident or action you feel sorry about?",
                 "How do you personally experience the feeling of sorry?",
                 "Is there anything you wish to do or say to address the situation?",
                 "Have you considered the impact of your actions and the possibility of making amends?"]
            ],
            [
                r"(.*)(yes|yeah|yep|yup|ya|sure|absolutely|definitely|certainly)(.*)",
                ["That's great to hear! What else can I assist you with?",
                "Wonderful! How can I be of further help to you?",
                "Fantastic! Is there anything specific you would like to know or discuss?",
                "Excellent! Feel free to ask me any questions you may have.",
                "Awesome! Let me know how I can assist you."]
            ],
            [
                r"(.*)(no|nope|nah|not (really|interested))(.*)",
                ["Alright, no problem. If you change your mind or have any questions, feel free to ask.",
                "Okay, understood. Let me know if there's anything else I can assist you with.",
                "Got it. If there's ever anything you'd like to know or discuss, feel free to reach out.",
                "Sure, no worries. If there's a different topic you'd like to explore, just let me know.",
                "I understand. If you ever need assistance in the future, don't hesitate to ask."]
            ],
            [
                r"(.*)(ok|okay|alright|sure|fine|got it|understood|understand|(.*)agree(.*)|(.*)accept(.*))(.*)",
                ["Alright, let's proceed. How can I assist you further?",
                "Great! If you have any specific questions or need guidance, feel free to ask.",
                "Perfect! Let me know what you'd like to explore or discuss.",
                "Okay, understood. If there's anything specific you'd like to know, just let me know.",
                "Got it. If you need any further information or support, feel free to reach out."]
            ],
            [
                r"(.*)",
                ["I kindly request you to provide further details.",
                 "I appreciate your input.",
                 "Would you be so kind as to elaborate on that?",
                 "I see. My algorithm is craving for more. Dish it out! ",
                 "Could you please provide more information?",
                 "I'm genuinely interested in learning more. Could you expand on that?",
                 "Your insights are valuable. Can you provide additional context?",
                 "I acknowledge your response. Can you go into more detail?",
                 "I'm actively listening. Please share more about your thoughts.",
                 "I'm here to assist you. Can you provide more information?"]
            ]
        ]
        # Initialize the chatbot
        self.chatbot = Chat(self.pairs, reflections)
        # Create a speech recognition instance
        self.recognizer = sr.Recognizer()
        # Register the route for the index page
        self.app.route("/", methods=['GET', 'POST'])(self.index)
        # Register the route for speech recognition
        self.app.route("/recognize", methods=['POST'])(self.recognize)

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Please speak something...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None

    def index(self):
        if request.method == "POST":
            userPrompt = request.json['message']
            print(userPrompt)

            if userPrompt == "start recognition":
                recognized_text = self.recognize_speech()
                if recognized_text:
                    return self.chat(recognized_text)
                else:
                    return "Sorry, I couldn't recognize any speech."

            return self.chat(userPrompt)
        else:
            return render_template("index.html")

    def recognize(self):
        recognized_text = self.recognize_speech()
        if recognized_text:
            return recognized_text
        else:
            return "Sorry, I couldn't recognize any speech."

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
