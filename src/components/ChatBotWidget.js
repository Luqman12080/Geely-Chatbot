import React, { useState } from 'react';
import { MessageCircle, Send } from 'lucide-react';
import Markdown from 'react-markdown'

function ChatBotWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            text: `Hello, I am a chatbot. I can help you find the right information and answer general questions about the available car models offered by Geely Motors. What would you like to know?`, isBot: true, date: new Date()
        }
    ]);
    const [inputUser, setInputUser] = useState('');

    const handleSend = async (e) => {
        e.preventDefault();
        if (!inputUser.trim()) return;

        const userMessage = { text: inputUser, isBot: false, date: new Date() };
        setMessages(prev => [...prev, userMessage]);
        setInputUser('');
        let result = null
        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ input: inputUser })
            })
            const data = await response.json()
            // console.log("Data: ", data.response)
            result = data.response
            // console.log("Response: ", data.answer)
        }
        catch (e) {
            console.log("Error: ", e)
        }

        // Simulate bot response
        setTimeout(() => {
            const botMessage = {
                text: result ? result : "Sorry, I don't understand that yet.",
                isBot: true,
                date: new Date()
            };
            setMessages(prev => [...prev, botMessage]);
        }, 1000);
    };

    return (
        <div className="chatbot-container">
            {!isOpen ? (
                <button
                    className="chat-button"
                    onClick={() => setIsOpen(true)}
                >
                    <MessageCircle size={24} />
                </button>
            ) : (
                <div className="chat-window">
                    <div className="chat-header">
                        <h3>Geely Virtual Assistant</h3>
                        <button
                            className="close-button"
                            onClick={() => setIsOpen(false)}
                        >
                            ×
                        </button>
                    </div>
                    <div className="messages">
                        {messages.map((message, index) => (
                            <div className='message-container' >
                                <div
                                    key={index}
                                    className={`message ${message.isBot ? 'bot' : 'user'}`}
                                >
                                    <Markdown>{message.text}</Markdown>
                                </div>
                                <div className={`${message.isBot ? 'botDate' : 'userDate'}`} >
                                    {message.date.toLocaleTimeString()}
                                </div>

                            </div>
                        ))}
                    </div>
                    <form onSubmit={handleSend} className="input-form">
                        <input
                            type="text"
                            value={inputUser}
                            onChange={(e) => setInputUser(e.target.value)}
                            placeholder="🚗 Type your message..."
                            className="message-input"
                        />
                        <button type="submit" className="send-button">
                            <Send size={20} />
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
}

export default ChatBotWidget;