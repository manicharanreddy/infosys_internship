import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/globals.css';
import './Dashboard.css';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      navigate('/login');
    } else {
      setUser(JSON.parse(userData));
    }
  }, [navigate]);

  if (!user) {
    return <div>Loading...</div>;
  }

  const toolDescriptions = [
    {
      name: "Resume Upload",
      icon: "📄",
      description: "Upload your resume in PDF, DOC, or DOCX format. Our AI parser will extract key information including your skills, experience, and education to help match you with suitable job opportunities."
    },
    {
      name: "Job Matching",
      icon: "💼",
      description: "Enter your target job role to see how well your resume matches. Get a detailed match score along with specific recommendations for improvement and skills you may be missing."
    },
    {
      name: "Career Path Simulator",
      icon: "📈",
      description: "Visualize your future career progression based on skills you currently have or plan to develop. See potential career paths and the steps needed to achieve your goals."
    },
    {
      name: "Future Skills Predictor",
      icon: "🔮",
      description: "Discover emerging skills in your industry before they peak. Stay ahead of trends and identify which skills to develop for better career prospects in the next 2-5 years."
    },
    {
      name: "Bias Checker",
      icon: "✅",
      description: "Ensure your resume uses inclusive language and is free from biased terms. Get suggestions to make your resume more appealing to diverse employers and ATS systems."
    },
    {
      name: "Portfolio Generator",
      icon: "📁",
      description: "Convert your resume information into a professional portfolio website. Generate project ideas and get templates to showcase your work effectively to potential employers."
    },
    {
      name: "Interview Practice",
      icon: "💬",
      description: "Prepare for interviews with AI-generated questions tailored to your target role. Practice your responses and get feedback to improve your interview performance."
    },
    {
      name: "AI Mentor Chat",
      icon: "🤖",
      description: "Get personalized career guidance, skill recommendations, and project ideas from our AI mentor based on your resume and career goals. Ask questions about career development, skill progression, and job market trends."
    }
  ];

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AI Career Platform Dashboard</h1>
      </header>

      <main className="dashboard-main">
        <section className="welcome-section">
          <h2>Your Career Development Hub</h2>
          <p>Leverage our AI-powered tools to enhance your career prospects and achieve your professional goals.</p>
          <p>Use the sidebar to navigate to different tools and features.</p>
        </section>

        <section className="tools-description-section">
          <h2>Platform Tools Overview</h2>
          <div className="tools-grid">
            {toolDescriptions.map((tool, index) => (
              <div className="tool-card" key={index}>
                <div className="tool-icon">{tool.icon}</div>
                <h3>{tool.name}</h3>
                <p>{tool.description}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;