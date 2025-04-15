document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // 显示用户消息
        addMessage(message, true);
        userInput.value = '';

        try {
            console.log('Sending message to server...');
            const response = await fetch('/chat/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: message }),
                // 添加超时设置
                signal: AbortSignal.timeout(60000) // 60秒超时
            });

            console.log('Response received:', response);
            const data = await response.json();
            console.log('Response data:', data);

            if (data.error) {
                addMessage(`服务暂时不可用，请稍后重试。错误信息：${data.error}`);
            } else {
                addMessage(data.response);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('网络连接不稳定，请检查网络后重试。');
        }
    }

    // 获取CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 添加事件监听器
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});