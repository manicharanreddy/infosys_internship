import React, { useState } from 'react';
import { checkBias } from '../services/api';
import './BiasChecker.css';

const BiasChecker = () => {
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [checkResult, setCheckResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isFileUploaded, setIsFileUploaded] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    
    if (selectedFile) {
      // For text files, read content directly
      if (selectedFile.type === 'text/plain' || selectedFile.name.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          setResumeText(event.target.result);
          setIsFileUploaded(true);
        };
        reader.readAsText(selectedFile);
      } else {
        // For other file types, we'll upload and process on the backend
        setIsFileUploaded(true);
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const selectedFile = e.dataTransfer.files[0];
      setFile(selectedFile);
      
      if (selectedFile) {
        // For text files, read content directly
        if (selectedFile.type === 'text/plain' || selectedFile.name.endsWith('.txt')) {
          const reader = new FileReader();
          reader.onload = (event) => {
            setResumeText(event.target.result);
            setIsFileUploaded(true);
          };
          reader.readAsText(selectedFile);
        } else {
          // For other file types, we'll upload and process on the backend
          setIsFileUploaded(true);
        }
      }
    }
  };

  const handleCheck = async (e) => {
    e.preventDefault();
    
    if (!isFileUploaded) {
      alert('Please upload a resume file first');
      return;
    }

    setLoading(true);
    try {
      let textToSend = resumeText;
      
      // If we don't have text content (PDF/DOCX), upload the file
      if (!resumeText && file) {
        const formData = new FormData();
        formData.append('resume', file);
        
        // First upload the file to get parsed content
        const uploadResponse = await fetch('http://localhost:5000/api/resume/upload', {
          method: 'POST',
          body: formData,
        });
        
        if (uploadResponse.ok) {
          const uploadData = await uploadResponse.json();
          if (uploadData.extractedInfo) {
            // Extract text content from parsed resume
            // This is a simplified approach - in a real implementation, 
            // you might want to reconstruct the full text from the parsed data
            const contactInfo = uploadData.extractedInfo.contact_info;
            const skills = uploadData.extractedInfo.skills;
            
            textToSend = `Name: ${contactInfo?.name || ''}\n`;
            if (contactInfo?.emails && contactInfo.emails.length > 0) {
              textToSend += `Email: ${contactInfo.emails[0]}\n`;
            }
            if (contactInfo?.phones && contactInfo.phones.length > 0) {
              textToSend += `Phone: ${contactInfo.phones[0]}\n`;
            }
            textToSend += `Skills: ${skills ? skills.join(', ') : ''}\n`;
            // Add more content reconstruction as needed
          }
        } else {
          throw new Error('Failed to upload and parse resume');
        }
      }
      
      if (!textToSend.trim()) {
        throw new Error('No resume content to analyze');
      }
      
      const response = await checkBias({ resumeText: textToSend });
      setCheckResult(response.data);
    } catch (error) {
      console.error('Bias check error:', error);
      setCheckResult({ error: 'Failed to check for bias: ' + error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCorrected = () => {
    if (checkResult && checkResult.correctedText) {
      const blob = new Blob([checkResult.correctedText], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'corrected-resume.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="bias-checker">
      <h2>Bias & Inclusivity Checker</h2>
      <form onSubmit={handleCheck}>
        <div 
          className={`file-upload-area ${isDragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="file-upload-icon">📄</div>
          <div className="file-upload-text">
            {file ? file.name : 'Drag & Drop your resume here'}
          </div>
          <div className="file-upload-hint">
            {file ? 'File selected' : 'Supports TXT, PDF, DOC, DOCX files (Max 5MB)'}
          </div>
          <input 
            type="file"
            id="resumeFile"
            accept=".txt,.pdf,.doc,.docx"
            onChange={handleFileChange}
            className="file-upload-input"
          />
        </div>
        {isFileUploaded && <p>File uploaded successfully. Click "Check for Bias" to analyze.</p>}
        
        <button type="submit" disabled={loading || !isFileUploaded}>
          {loading ? 'Checking...' : 'Check for Bias'}
        </button>
      </form>
      
      {checkResult && (
        <div className="check-result">
          <h3>Bias Check Results</h3>
          <p>Word Count: {checkResult.wordCount}</p>
          
          <div className="bias-issues-container">
            <h4>🔍 Potential Bias Issues Found:</h4>
            {checkResult.biasIssues.length > 0 ? (
              <div className="issues-grid">
                {checkResult.biasIssues.map((issue, index) => (
                  <div key={index} className="issue-card">
                    <div className="issue-header">
                      <span className="issue-term">{issue.term}</span>
                      <span className="issue-category" style={{
                        backgroundColor: issue.category === 'Gender' ? '#f59e0b' : 
                                      issue.category === 'Age' ? '#ef4444' : 
                                      issue.category === 'Race' ? '#8b5cf6' : 
                                      '#0ea5e9'
                      }}>
                        {issue.category}
                      </span>
                    </div>
                    <div className="issue-content">
                      <p className="issue-suggestion">💡 <strong>Suggestion:</strong> {issue.suggestion}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-issues">
                <div className="success-icon">✅</div>
                <p>No obvious bias terms detected.</p>
              </div>
            )}
          </div>
          
          <div className="pronouns-section">
            <h4>👥 Gender Pronoun Usage:</h4>
            <div className="pronouns-stats">
              <div className="stat-card">
                <div className="stat-value">{checkResult.genderPronouns.masculine}</div>
                <div className="stat-label">Masculine</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{checkResult.genderPronouns.feminine}</div>
                <div className="stat-label">Feminine</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{checkResult.genderPronouns.neutral}</div>
                <div className="stat-label">Neutral</div>
              </div>
            </div>
          </div>
          
          <div className="improvement-suggestions">
            <h4>✨ Suggestions for Improvement:</h4>
            <div className="suggestions-list">
              {checkResult.suggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-item">
                  <span className="suggestion-number">{index + 1}.</span>
                  <span className="suggestion-text">{suggestion}</span>
                </div>
              ))}
            </div>
          </div>
          
          {checkResult.correctedText && (
            <div className="corrected-resume-section">
              <h4>📄 Corrected Resume:</h4>
              <div className="download-card">
                <div className="download-info">
                  <p>Your resume has been corrected for bias and inclusivity.</p>
                </div>
                <button type="button" onClick={handleDownloadCorrected} className="download-button">
                  📥 Download Corrected Resume
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default BiasChecker;