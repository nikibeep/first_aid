document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const chatContent = document.getElementById('chat-content');
    const userInputElement = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const recordButton = document.getElementById('record-button');
    const audioFileInput = document.getElementById('audio-file');
    const responseAudio = document.getElementById('response-audio');
    const chatForm = document.getElementById('chat-form');
    const audioFileHiddenInput = document.getElementById('audio-file-hidden');

    // Function to append a new chat bubble to the chat content
    function appendChatBubble(message, sender) {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble ' + sender + '-bubble';
        bubble.textContent = message;
        chatContent.appendChild(bubble);

        // Scroll to the bottom of the chat content
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    // Function to handle user input
    function handleUserInput() {
        const userInput = userInputElement.value;
        if (userInput.trim() === '') return;

        appendChatBubble(userInput, 'user');
        userInputElement.value = ''; // Clear the input field

        // Send the user input to the server for processing
        fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: userInput }),
        })
        .then(response => response.json())
        .then(data => {
            appendChatBubble(data.response, 'bot');
            if (data.audio_url) {
                responseAudio.src = data.audio_url;
                responseAudio.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error processing text:', error);
        });
    }

    // Function to handle audio file input
    function handleAudioFileInput() {
        const file = audioFileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('audio', file);

        fetch('/process_uploaded_audio', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            responseAudio.src = 'static/response.mp3';
            responseAudio.style.display = 'block';
        })
        .catch(error => {
            console.error('Error processing audio:', error);
        });
    }

    sendButton.addEventListener('click', handleUserInput);
    userInputElement.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleUserInput();
        }
    });

    recordButton.addEventListener('click', () => {
        audioFileInput.click();
    });

    audioFileInput.addEventListener('change', handleAudioFileInput);

    chatForm.addEventListener('submit', event => {
        event.preventDefault();
        audioFileHiddenInput.value = audioFileInput.value;
        chatForm.submit();
    });
});
