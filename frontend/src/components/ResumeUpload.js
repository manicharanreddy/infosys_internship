import React, { useState } from 'react';
import { uploadResume } from '../services/api';
import './ResumeUpload.css';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [jobRecommendations, setJobRecommendations] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
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
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      alert('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    setUploading(true);
    try {
      const response = await uploadResume(formData);
      setUploadResult(response.data);
      
      // Pass the extracted info to the parent component
      if (response.data.extractedInfo && onUploadSuccess) {
        onUploadSuccess(response.data.extractedInfo);
      }
      
      // Get job recommendations based on extracted skills
      if (response.data.extractedInfo && response.data.extractedInfo.skills) {
        // In a real implementation, this would call a backend endpoint
        // For now, we'll simulate recommendations based on skills
        const skills = response.data.extractedInfo.skills;
        const recommendations = [
          {
            title: "Software Engineer",
            match_score: 85,
            matching_skills: skills.slice(0, Math.min(5, skills.length)),
            missing_skills: ["Team Leadership", "Project Management"]
          },
          {
            title: "Frontend Developer",
            match_score: 78,
            matching_skills: skills.filter(skill => 
              skill.toLowerCase().includes('javascript') || 
              skill.toLowerCase().includes('react') || 
              skill.toLowerCase().includes('html') || 
              skill.toLowerCase().includes('css')
            ),
            missing_skills: ["Vue.js", "Angular"]
          },
          {
            title: "Backend Developer",
            match_score: 72,
            matching_skills: skills.filter(skill => 
              skill.toLowerCase().includes('python') || 
              skill.toLowerCase().includes('node') || 
              skill.toLowerCase().includes('database') || 
              skill.toLowerCase().includes('sql')
            ),
            missing_skills: ["Microservices", "Docker"]
          }
        ];
        setJobRecommendations(recommendations);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadResult({ error: 'Upload failed: ' + (error.response?.data?.error || error.message) });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>Upload Your Resume</h2>
      <form onSubmit={handleUpload}>
        <div 
          className={`file-upload-area ${isDragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="file-upload-icon">📁</div>
          <div className="file-upload-text">
            {file ? file.name : 'Drag & Drop your resume here'}
          </div>
          <div className="file-upload-hint">
            {file ? 'File selected' : 'Supports PDF, DOC, DOCX files (Max 5MB)'}
          </div>
          <input 
            type="file" 
            accept=".pdf,.doc,.docx" 
            onChange={handleFileChange} 
            className="file-upload-input"
          />
        </div>
        <button type="submit" disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload Resume'}
        </button>
      </form>
      
      {uploadResult && (
        <div className="upload-result">
          <h3>Upload Result:</h3>
          <p>{uploadResult.message}</p>
          {uploadResult.filename && <p>File: {uploadResult.filename}</p>}
          
          {uploadResult.extractedInfo && (
            <div className="extracted-info">
              <h4>Extracted Information:</h4>
              {uploadResult.extractedInfo.contact_info && (
                <div className="contact-info-section">
                  <h5>👤 Contact Information</h5>
                  <div className="contact-details">
                    <div className="contact-item">
                      <span className="contact-label">Name:</span>
                      <span className="contact-value">{uploadResult.extractedInfo.contact_info.name}</span>
                    </div>
                    {uploadResult.extractedInfo.contact_info.emails && uploadResult.extractedInfo.contact_info.emails.length > 0 && (
                      <div className="contact-item">
                        <span className="contact-label">Email:</span>
                        <span className="contact-value">{uploadResult.extractedInfo.contact_info.emails[0]}</span>
                      </div>
                    )}
                    {uploadResult.extractedInfo.contact_info.phones && uploadResult.extractedInfo.contact_info.phones.length > 0 && (
                      <div className="contact-item">
                        <span className="contact-label">Phone:</span>
                        <span className="contact-value">{uploadResult.extractedInfo.contact_info.phones[0]}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {uploadResult.extractedInfo.skills && uploadResult.extractedInfo.skills.length > 0 && (
                <div className="skills-section">
                  <h5>🛠 Skills ({uploadResult.extractedInfo.skills.length})</h5>
                  <div className="skills-grid">
                    {uploadResult.extractedInfo.skills.map((skill, index) => (
                      <div key={index} className="skill-badge">
                        <span className="skill-text">{skill}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {jobRecommendations && jobRecommendations.length > 0 && (
                <div>
                  <h5>Suitable Job Roles for Your Skills:</h5>
                  <div className="job-recommendations">
                    {jobRecommendations.map((job, index) => (
                      <div key={index} className="job-recommendation">
                        <h6>{job.title} - Match Score: {job.match_score}%</h6>
                        <p>Matching Skills: {job.matching_skills.join(', ')}</p>
                        <p>Missing Skills to Learn: {job.missing_skills.join(', ')}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
          {uploadResult.error && <p className="error">Error: {uploadResult.error}</p>}
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;