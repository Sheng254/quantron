// Get DOM elements
const chatlog = document.getElementById('chatlog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const micButton = document.getElementById('micButton');

// Event listener for send button click
sendButton.addEventListener('click', handleUserInput);

// Event listener for user input enter key press
userInput.addEventListener('keyup', function (event) {
    if (event.keyCode === 13) {
        handleUserInput();
    }
});

// Event listener for mic button click
micButton.addEventListener('click', handleMicButtonClick);

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

// Function to handle mic button click
function handleMicButtonClick() {
    // Request speech input from the user
    recognition.start();
}

// Create a SpeechRecognition object
const recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

// Event listener for speech recognition result
recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    displayUserMessage(transcript);
    sendUserMessageToServer(transcript);
};

// Function to display user message in the chat log
function displayUserMessage(message) {
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');
    userMessageElement.innerText = "🤔 : " + message;
    chatlog.appendChild(userMessageElement);
}

// Function to display bot message in the chat log
function displayBotMessage(message) {
    const botMessageElement = document.createElement('div');
    botMessageElement.classList.add('bot-message');
    botMessageElement.innerHTML = "🤖 : " + message;
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
