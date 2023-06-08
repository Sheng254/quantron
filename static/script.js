// Get DOM elements
const chatlog = document.getElementById('chatlog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');

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
    const initialBotMessage = "Welcome to Quantron, your personal assistant!";
    const instructionMessage = "To begin, type your messages in the chat. I'm here to assist you.";
    displayBotMessage(initialBotMessage);
    displayBotMessage(instructionMessage);
}

// Display the initial bot message
const initialBotMessage = "Welcome to Quantron, your personal assistant!";
const instructionMessage = "To begin, type your messages in the chat. I'm here to assist you.";
displayBotMessage(initialBotMessage);
displayBotMessage(instructionMessage);
