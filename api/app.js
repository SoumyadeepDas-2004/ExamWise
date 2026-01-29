// State management
let conversationHistory = [];
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('input');
    if (input) input.focus();
});

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        send();
    }
}

// Send message
async function send() {
    const input = document.getElementById('input');
    const chat = document.getElementById('chat');
    const text = input.value.trim();

    if (!text || isLoading) return;

    // Remove welcome section if this is the first message
    const welcomeSection = chat.querySelector('.welcome-section');
    if (welcomeSection) {
        welcomeSection.remove();
    }

    // Add user message to UI
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'msg user';
    userMessageDiv.innerHTML = `<div>${escapeHtml(text)}</div>`;
    chat.appendChild(userMessageDiv);

    // Clear input and scroll
    input.value = '';
    chat.scrollTop = chat.scrollHeight;

    // Add bot "thinking" message
    const botThinkingDiv = document.createElement('div');
    botThinkingDiv.className = 'msg bot';
    botThinkingDiv.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
    chat.appendChild(botThinkingDiv);
    chat.scrollTop = chat.scrollHeight;

    isLoading = true;
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    try {
        // Send request to backend
        const res = await fetch('http://127.0.0.1:8000/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        
        // Replace thinking message with actual response
        const botMessage = data.answer || 'No response received.';
        
        // Parse markdown to HTML
        const marked = window.marked; // Declare the marked variable
        const htmlMessage = marked.parse(botMessage);
        botThinkingDiv.innerHTML = `<div>${htmlMessage}</div>`;

        // Store in conversation history
        conversationHistory.push({
            role: 'user',
            content: text
        });
        conversationHistory.push({
            role: 'assistant',
            content: botMessage
        });

    } catch (error) {
        console.error('Error:', error);
        const errorMessage = `Sorry, I encountered an error: ${error.message}. Make sure your backend server is running at http://127.0.0.1:8000`;
        botThinkingDiv.innerHTML = `<div>${escapeHtml(errorMessage)}</div>`;
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        chat.scrollTop = chat.scrollHeight;
        input.focus();
    }
}

// Send message from suggestion cards
function sendMessage(message) {
    const input = document.getElementById('input');
    input.value = message;
    send();
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Add typing animation styles dynamically
const style = document.createElement('style');
style.textContent = `
    .typing {
        display: flex;
        gap: 4px;
        align-items: center;
    }

    .typing span {
        width: 8px;
        height: 8px;
        background-color: currentColor;
        border-radius: 50%;
        animation: typingAnimation 1.4s infinite;
    }

    .typing span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typingAnimation {
        0%, 60%, 100% {
            opacity: 0.5;
            transform: translateY(0);
        }
        30% {
            opacity: 1;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);
