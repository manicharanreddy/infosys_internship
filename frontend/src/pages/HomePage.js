import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/login');
  };

  return (
    <div className="home-page">
      <header className="home-header">
        <h1>AI Career Platform</h1>
        <p>Your AI-powered career development platform</p>
      </header>

      <section className="hero-section">
        <div className="hero-content">
          <h2>Transform Your Career with AI</h2>
          <p>
            Our platform leverages cutting-edge artificial intelligence to help you optimize your resume, 
            discover suitable job opportunities, and plan your career path effectively.
          </p>
          <button className="cta-button" onClick={handleGetStarted}>
            Get Started
          </button>
        </div>
      </section>

      <section className="features-section">
        <h2>Our Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Resume Upload & Parsing</h3>
            <p>Upload resumes in PDF, DOC, or DOCX formats with automatic parsing and extraction of key information.</p>
          </div>
          
          <div className="feature-card">
            <h3>Job Role Matching</h3>
            <p>Enter a job role to see how well your resume matches and get recommendations for improvement.</p>
          </div>
          
          <div className="feature-card">
            <h3>AI Career Path Simulator</h3>
            <p>See future career outcomes based on skills you add/learn with step-by-step progression guidance.</p>
          </div>
          
          <div className="feature-card">
            <h3>Future Skill Predictor</h3>
            <p>Predict upcoming in-demand skills before they peak to stay ahead of industry trends.</p>
          </div>
          
          <div className="feature-card">
            <h3>Bias & Inclusivity Checker</h3>
            <p>Ensure your resume is free of biased or non-inclusive language with improvement suggestions.</p>
          </div>
          
          <div className="feature-card">
            <h3>AI Portfolio Generator</h3>
            <p>Convert resume information into a professional portfolio with project ideas and website generation.</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to Transform Your Career?</h2>
        <p>Join thousands of professionals who have already enhanced their career prospects with our AI platform.</p>
        <button className="cta-button" onClick={handleGetStarted}>
          Get Started Now
        </button>
      </section>
    </div>
  );
};

export default HomePage;