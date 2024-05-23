import { marked } from 'marked';
import React, { useEffect, useRef, useState } from 'react';
import { getAIMessage } from '../api/api';
import { ASSISTANT_ROLE, USER_ROLE } from '../constants/role';
import './ChatWindow.css';

const defaultMessage = [
  {
    role: ASSISTANT_ROLE,
    content:
      'Hello there, my name is Shree and I will be your virtual assistant today. Currently, my capabilities are limited to assisting you with either refrigerators or dishwashers only. How can I help you today?',
  },
];

function ChatWindow() {
  const [messages, setMessages] = useState([...defaultMessage]);
  const [input, setInput] = useState('');
  const [aiThinking, setAIThinking] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '' || aiThinking) {
      return;
    }

    const newUserMessage = { role: USER_ROLE, content: input };
    const updatedMessages = [...messages, newUserMessage];

    setMessages(updatedMessages);
    setInput('');

    // Call API & set assistant message
    setAIThinking(true);
    const newMessage = await getAIMessage(updatedMessages).finally(() =>
      setAIThinking(false)
    );

    setMessages((prevMessages) => [
      ...prevMessages,
      { role: ASSISTANT_ROLE, content: newMessage },
    ]);
  };

  return (
    <div className='messages-container'>
      {messages.map((message, index) => (
        <div key={index} className={`${message.role}-message-container`}>
          {message.content && (
            <div className={`message ${message.role}-message`}>
              <div
                dangerouslySetInnerHTML={{
                  __html: marked(message.content).replace(/<p>|<\/p>/g, ''),
                }}
              ></div>
            </div>
          )}
        </div>
      ))}
      {aiThinking && (
        <div
          className={`message ${ASSISTANT_ROLE}-message`}
          style={{ opacity: 0.5 }}
        >
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'start',
            gap: '10px',
          }}> 
            <div className='loader' />
            Thinking ...
          </div>

        </div>
      )}
      <div ref={messagesEndRef} />
      <div className='input-area'>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Type a message...'
          onKeyUp={(e) => {
            if (e.key !== 'Enter' || e.shiftKey) {
              return;
            }
            handleSend();
            e.preventDefault();
          }}
          rows='3'
          disabled={aiThinking}
          style={{
            cursor: aiThinking ? 'not-allowed' : 'default',
            opacity: aiThinking ? 0.5 : 1,
          }}
        />
        <button
          className='send-button'
          onClick={handleSend}
          disabled={aiThinking}
          style={{
            cursor: aiThinking ? 'not-allowed' : 'default',
            opacity: aiThinking ? 0.5 : 1,
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
