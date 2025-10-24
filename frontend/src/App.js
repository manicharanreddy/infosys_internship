import React, { useState, useEffect } from 'react';
import ResumeUpload from './components/ResumeUpload';
import JobMatching from './components/JobMatching';
import CareerPathSimulator from './components/CareerPathSimulator';
import FutureSkillPredictor from './components/FutureSkillPredictor';
import BiasChecker from './components/BiasChecker';
import PortfolioGenerator from './components/PortfolioGenerator';
import InterviewPractice from './components/InterviewPractice';
import './styles/globals.css';
import './styles/App.css';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [resumeSkills, setResumeSkills] = useState([]);
  const [resumeData, setResumeData] = useState(null);

  useEffect(() => {
    // Create floating background elements
    const createFloatingShapes = () => {
      const container = document.body;
      for (let i = 0; i < 4; i++) {
        const shape = document.createElement('div');
        shape.className = 'floating-shape';
        container.appendChild(shape);
      }
    };

    createFloatingShapes();

    // Cleanup function
    return () => {
      const shapes = document.querySelectorAll('.floating-shape');
      shapes.forEach(shape => shape.remove());
    };
  }, []);

  const handleUploadSuccess = (extractedInfo) => {
    if (extractedInfo.skills) {
      setResumeSkills(extractedInfo.skills);
    }
    setResumeData(extractedInfo);
  };

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'upload':
        return <ResumeUpload onUploadSuccess={handleUploadSuccess} />;
      case 'matching':
        return <JobMatching resumeSkills={resumeSkills} />;
      case 'career':
        return <CareerPathSimulator resumeSkills={resumeSkills} />;
      case 'skills':
        return <FutureSkillPredictor resumeSkills={resumeSkills} />;
      case 'bias':
        return <BiasChecker />;
      case 'portfolio':
        return <PortfolioGenerator resumeData={resumeData} />;
      case 'interview':
        return <InterviewPractice resumeData={resumeData} />;
      default:
        return <ResumeUpload onUploadSuccess={handleUploadSuccess} />;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Career Platform</h1>
        <p>Your AI-powered career development platform</p>
      </header>
      
      <nav className="main-nav">
        <ul>
          <li>
            <button 
              className={activeTab === 'upload' ? 'active' : ''} 
              onClick={() => setActiveTab('upload')}
            >
              Resume Upload
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'matching' ? 'active' : ''} 
              onClick={() => setActiveTab('matching')}
            >
              Job Matching
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'career' ? 'active' : ''} 
              onClick={() => setActiveTab('career')}
            >
              Career Path
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'skills' ? 'active' : ''} 
              onClick={() => setActiveTab('skills')}
            >
              Future Skills
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'bias' ? 'active' : ''} 
              onClick={() => setActiveTab('bias')}
            >
              Bias Checker
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'portfolio' ? 'active' : ''} 
              onClick={() => setActiveTab('portfolio')}
            >
              Portfolio Generator
            </button>
          </li>
          <li>
            <button 
              className={activeTab === 'interview' ? 'active' : ''} 
              onClick={() => setActiveTab('interview')}
            >
              Interview Practice
            </button>
          </li>
        </ul>
      </nav>
      
      <main className="main-content">
        {renderActiveComponent()}
      </main>
    </div>
  );
}

export default App;