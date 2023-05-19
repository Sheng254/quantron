// Get DOM elements
const chatlog = document.getElementById('chatlog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// Event listener for send button click
sendButton.addEventListener('click', handleUserInput);

// Event listener for user input enter key press
userInput.addEventListener('keyup', function (event) {
    if (event.keyCode === 13) {
        handleUserInput();
    }
});

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
    botMessageElement.innerText = message;
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
