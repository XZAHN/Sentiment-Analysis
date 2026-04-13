document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatContainer = document.getElementById('chatContainer');

    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const paragraph = document.createElement('p');
        paragraph.textContent = content;
        contentDiv.appendChild(paragraph);

        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);

        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to send message to backend
    async function sendMessage(text) {
        try {
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            return data.sentiment;
        } catch (error) {
            console.error('Error:', error);
            return 'Error: Could not analyze sentiment. Please try again.';
        }
    }

    // Function to handle sending a message
    async function handleSendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        // Add user message
        addMessage(text, true);

        // Clear input
        messageInput.value = '';
        sendButton.disabled = true;

        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-content">
                <p>Analyzing sentiment...</p>
            </div>
        `;
        chatContainer.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Get prediction
        const sentiment = await sendMessage(text);

        // Remove typing indicator
        chatContainer.removeChild(typingDiv);

        // Add bot response
        let responseText;
        if (sentiment === 1) {
            responseText = 'This text appears to have a positive sentiment! 😊';
        } else if (sentiment === 0) {
            responseText = 'This text appears to have a negative sentiment. 😔';
        } else {
            responseText = sentiment; // Error message
        }

        addMessage(responseText);

        sendButton.disabled = false;
        messageInput.focus();
    }

    // Event listeners
    sendButton.addEventListener('click', handleSendMessage);

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Enable/disable send button based on input
    messageInput.addEventListener('input', function() {
        sendButton.disabled = !this.value.trim();
    });

    // Initial focus
    messageInput.focus();
});