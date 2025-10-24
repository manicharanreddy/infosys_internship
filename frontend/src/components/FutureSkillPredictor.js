import React, { useState, useEffect } from 'react';
import { predictFutureSkills } from '../services/api';
import './FutureSkillPredictor.css';

const FutureSkillPredictor = ({ resumeSkills = [] }) => {
  const [skills, setSkills] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [availableSkills, setAvailableSkills] = useState([]);

  // Fetch available skills when component mounts
  useEffect(() => {
    // In a real implementation, this would fetch from the backend
    // For now, we'll use common skills
    const commonSkills = [
      'Python', 'JavaScript', 'React', 'Node.js', 'Java', 'C++', 'C#',
      'Machine Learning', 'Data Science', 'Artificial Intelligence',
      'Cloud Computing', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
      'Cybersecurity', 'DevOps', 'SQL', 'MongoDB', 'PostgreSQL',
      'HTML', 'CSS', 'Vue.js', 'Angular', 'TensorFlow', 'PyTorch'
    ];
    setAvailableSkills(commonSkills);
    
    // Set default skills if resume skills are available
    if (resumeSkills.length > 0) {
      setSkills(resumeSkills.join(', '));
    }
  }, [resumeSkills]);

  const handlePredict = async (e) => {
    e.preventDefault();
    
    if (!skills.trim()) {
      alert('Please enter your skills');
      return;
    }

    setLoading(true);
    try {
      const response = await predictFutureSkills({ skills });
      setPredictionResult(response.data);
    } catch (error) {
      console.error('Prediction error:', error);
      setPredictionResult({ error: 'Failed to predict future skills: ' + (error.response?.data?.error || error.message) });
    } finally {
      setLoading(false);
    }
  };

  const handleSkillChange = (e) => {
    const selectedSkill = e.target.value;
    if (selectedSkill && !skills.includes(selectedSkill)) {
      const newSkills = skills ? `${skills}, ${selectedSkill}` : selectedSkill;
      setSkills(newSkills);
    }
  };

  return (
    <div className="future-skill-predictor">
      <h2>Future Skill Predictor (2-5 Year Forecast)</h2>
      <form onSubmit={handlePredict}>
        <div>
          <label htmlFor="skills">Current Skills:</label>
          <div className="skills-input-container">
            <select
              id="skills"
              onChange={handleSkillChange}
              disabled={loading}
            >
              <option value="">Select skills to add...</option>
              {availableSkills.map((skill, index) => (
                <option key={index} value={skill}>{skill}</option>
              ))}
            </select>
            <input
              type="text"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="Selected skills will appear here (comma separated)"
              readOnly
            />
          </div>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Predicting with ML...' : 'Predict Future Skills'}
        </button>
      </form>
      
      {predictionResult && (
        <div className="prediction-result">
          {predictionResult.error ? (
            <p className="error">Error: {predictionResult.error}</p>
          ) : (
            <>
              <h3>Future Skills Forecast</h3>
              <p>Based on your current skills: {predictionResult.currentSkills.join(', ')}</p>
              
              <div className="predictions-container">
                <h4>🔮 Predicted In-Demand Skills (ML-Powered)</h4>
                <div className="predictions-grid">
                  {predictionResult.predictions.map((prediction, index) => (
                    <div key={index} className="prediction-card">
                      <div className="prediction-header">
                        <h5 className="skill-name">{prediction.skill}</h5>
                        <div className="growth-indicator">
                          <span className="growth-value">{prediction.growth_rate}%</span>
                          <span className="growth-label">Growth</span>
                        </div>
                      </div>
                      <div className="prediction-content">
                        <div className="trend-badge" style={{
                          backgroundColor: prediction.trend.includes('rapidly') ? 'var(--danger-color)' : 
                                        prediction.trend.includes('steadily') ? 'var(--warning-color)' : 
                                        'var(--success-color)'
                        }}>
                          {prediction.trend}
                        </div>
                        <p className="prediction-description">{prediction.description}</p>
                        {prediction.similarity_score && (
                          <div className="similarity-meter">
                            <span className="similarity-label">Similarity Score:</span>
                            <div className="similarity-bar">
                              <div 
                                className="similarity-fill" 
                                style={{ width: `${prediction.similarity_score * 10}%` }}
                              ></div>
                            </div>
                            <span className="similarity-value">{prediction.similarity_score}/10</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default FutureSkillPredictor;