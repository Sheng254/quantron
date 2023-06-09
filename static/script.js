// Get DOM elements
const chatlog = document.getElementById('chatlog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');
const authenticationSection = document.getElementById('authentication');
const yesButton = document.getElementById('yesButton');
const noButton = document.getElementById('noButton');
const chatbotContainer = document.getElementById('chatbotContainer');

// Event listener for "Yes" button click
yesButton.addEventListener('click', function() {
    authenticationSection.style.display = 'none';
    chatbotContainer.style.display = 'block';
});

// Event listener for "No" button click
noButton.addEventListener('click', function() {
    // Clear the page content
    document.body.innerHTML = '';
    document.body.style.background = 'black';

    // Create a new element for the message
    var messageElement = document.createElement('div');
    messageElement.innerText = `Apologies, access denied. Only individuals of the human kind are granted permission.\nKindly refresh the page and attempt to authenticate yourself again if you are a human user.`;
    messageElement.style.color = 'white';
    messageElement.style.textAlign = 'center';
    messageElement.style.marginTop = '50vh';
    messageElement.style.fontSize = '30px';
    document.body.appendChild(messageElement);
});

// Array of prompts
const prompts = [
    "How are you?",
    "Tell me a quote",
    "Tell me a joke",
    "Translate how are you to malay",
    "Gender Brandon",
    "Nationality May",
    "Suggest me an activity",
    "Calculate 100/14894-320"
];

// Function to add prompts to the chat log
function addPrompts() {
    const promptsContainer = document.getElementById("promptsContainer");

    prompts.forEach(function (promptText) {
        const promptElement = document.createElement("div");
        promptElement.classList.add("message-text");
        promptElement.textContent = promptText;
        promptElement.addEventListener("click", function () {
            sendMessage(promptText); // Send the prompt as a user message
            promptElement.classList.add("disabled"); // Optionally disable the prompt after clicking
        });

        promptsContainer.appendChild(promptElement);
    });
}

// Function to send a message to the chatbot
function sendMessage(message) {
    displayUserMessage(message);
    sendUserMessageToServer(message);
}

// Call the addPrompts function to populate the prompts
addPrompts();

// Event listener for send button click
sendButton.addEventListener('click', handleUserInput);

// Event listener for user input enter key press
userInput.addEventListener('keyup', function (event) {
    if (event.keyCode === 13) {
        handleUserInput();
    }
});

// Event listener for clear button click
clearButton.addEventListener('click', clearChat);

// Function to handle user input
function handleUserInput() {
    const message = userInput.value.trim();

    if (message !== '') {
        displayUserMessage(message);
        sendUserMessageToServer(message);

        // Clear the user input
        userInput.value = '';
    }
}

// Function to display user message in the chat log
function displayUserMessage(message) {
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');
    userMessageElement.innerText = message;
    chatlog.appendChild(userMessageElement);
}

// Function to display bot message in the chat log
function displayBotMessage(message) {
    const botMessageElement = document.createElement('div');
    botMessageElement.classList.add('bot-message');
    botMessageElement.innerHTML = message;
    chatlog.appendChild(botMessageElement);
}

// Function to send user message to the server
function sendUserMessageToServer(message) {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.text())
    .then(text => {
        console.log(text);
        displayBotMessage(text);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to clear the chat history and restart the conversation
function clearChat() {
    // Remove all child nodes from the chatlog
    while (chatlog.firstChild) {
        chatlog.removeChild(chatlog.firstChild);
    }

    // Display the initial bot message again
    const initialBotMessage = "👋 Welcome to Quantron, your personal assistant! 🚀";
    const instructionMessage = "💬 To begin, type your messages in the chat. I'm here to assist you. 🤝";
    displayBotMessage(initialBotMessage);
    displayBotMessage(instructionMessage);
}

// Display the initial bot message
const initialBotMessage = "👋 Welcome to Quantron, your personal assistant! 🚀";
const instructionMessage = "💬 To begin, type your messages in the chat. I'm here to assist you. 🤝";
displayBotMessage(initialBotMessage);
displayBotMessage(instructionMessage);
