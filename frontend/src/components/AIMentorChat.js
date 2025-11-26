import React, { useState, useEffect, useRef } from 'react';
import { getAIMentorResponse } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './AIMentorChat.css';

const AIMentorChat = ({ resumeData }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI Career Mentor. I can help you with career advice, skill development, project ideas, and more. What would you like to know?",
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check if resume data is available, if not prompt user to upload resume
  useEffect(() => {
    if (!resumeData) {
      setMessages(prev => [
        ...prev,
        {
          id: prev.length + 1,
          text: "I notice you haven't uploaded a resume yet. For personalized career advice, I recommend uploading your resume first. You can do this by navigating to the 'Resume Upload' section. However, you can still ask general career questions!",
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    }
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare data for API call
      const requestData = {
        query: inputValue,
        resumeData: resumeData || {
          skills: [],
          experience: "",
          education: "",
          projects: ""
        }
      };

      // Get AI response
      const response = await getAIMentorResponse(requestData);

      // Add AI response to chat
      const aiMessage = {
        id: messages.length + 2,
        text: response.data.response || response.data || "I'm here to help with your career questions!",
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error getting AI mentor response:', error);
      
      const errorMessage = {
        id: messages.length + 2,
        text: "Sorry, I'm having trouble responding right now. Please try again later.",
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const handleResumeUploadRedirect = () => {
    navigate('/resume-upload');
  };

  return (
    <div className="ai-mentor-chat">
      <div className="chat-header">
        <h2>🤖 AI Career Mentor</h2>
        <p>Get personalized career guidance based on your resume and career goals</p>
        {!resumeData && (
          <div className="resume-prompt">
            <p>No resume data found. For personalized advice, please upload your resume.</p>
            <button onClick={handleResumeUploadRedirect} className="upload-resume-button">
              Upload Resume
            </button>
          </div>
        )}
        <p className="mentor-description">Ask me about career paths, skill development, project ideas, interview preparation, and industry trends. I provide tailored advice based on your experience and aspirations.</p>
      </div>
      
      <div className="chat-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.sender}`}
          >
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-time">{message.timestamp}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message ai">
            <div className="message-content">
              <div className="message-text typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask your career question here... (e.g. 'What skills should I learn to become a Data Scientist?', 'How can I transition to a ML Engineer role?', 'What projects can I build to prove my React skills?')"
            disabled={isLoading}
            rows="3"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputValue.trim()}
            className="send-button"
          >
            {isLoading ? 'Thinking...' : 'Send'}
          </button>
        </div>
        <div className="input-hint">
          <p>Examples: "Which project can I build to prove my SQL skill?" or "How can I transition to a ML Engineer role?"</p>
        </div>
      </form>
    </div>
  );
};

export default AIMentorChat;