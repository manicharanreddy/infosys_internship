const fs = require('fs');
const path = require('path');
const { parseResume, matchJob, getJobRecommendations } = require('../utils/python_bridge');

// Handle resume upload and processing
const uploadResume = async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }
  
  try {
    // Determine file type
    let fileType = 'text';
    if (req.file.mimetype === 'application/pdf') {
      fileType = 'pdf';
    } else if (req.file.mimetype === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
      fileType = 'docx';
    }
    
    // Call Python script to parse resume
    const parsedData = await parseResume(req.file.path, fileType);
    
    if (parsedData.error) {
      return res.status(500).json({ error: parsedData.error });
    }
    
    res.json({
      success: true,
      filename: req.file.filename,
      message: 'Resume uploaded and parsed successfully',
      extractedInfo: parsedData
    });
  } catch (error) {
    console.error('Resume processing error:', error);
    res.status(500).json({ error: 'Failed to process resume: ' + error.message });
  }
};

// Get job match score
const getJobMatch = async (req, res) => {
  try {
    const { jobRole, resumeSkills } = req.body;
    
    // Call Python script to calculate match score
    const matchResult = await matchJob(resumeSkills, jobRole);
    
    if (matchResult.error) {
      return res.status(500).json({ error: matchResult.error });
    }
    
    res.json(matchResult);
  } catch (error) {
    console.error('Job matching error:', error);
    res.status(500).json({ error: 'Failed to calculate job match: ' + error.message });
  }
};

// Simulate career path
const simulateCareerPath = async (req, res) => {
  try {
    const { skills, desiredRole } = req.body;
    const skillsArray = skills.split(',').map(skill => skill.trim()).filter(skill => skill);
    
    // Call Python script to get job recommendations
    const recommendations = await getJobRecommendations(skillsArray);
    
    // For career path simulation, we'll still use a mock approach but with real data
    const mockResult = {
      currentSkills: skillsArray,
      desiredRole: desiredRole,
      careerPath: [
        {
          step: 1,
          role: `Junior ${desiredRole}`,
          timeframe: '0-2 years',
          requiredSkills: skillsArray.slice(0, Math.max(1, Math.floor(skillsArray.length/2))),
          skillsToAcquire: ['Communication', 'Problem Solving']
        },
        {
          step: 2,
          role: desiredRole,
          timeframe: '2-5 years',
          requiredSkills: [...skillsArray, 'Communication', 'Problem Solving'],
          skillsToAcquire: ['Leadership', 'Project Management']
        },
        {
          step: 3,
          role: `Senior ${desiredRole}`,
          timeframe: '5-10 years',
          requiredSkills: [...skillsArray, 'Communication', 'Problem Solving', 'Leadership', 'Project Management'],
          skillsToAcquire: ['Strategic Thinking', 'Executive Communication']
        }
      ],
      jobRecommendations: recommendations
    };
    
    res.json(mockResult);
  } catch (error) {
    console.error('Career simulation error:', error);
    res.status(500).json({ error: 'Failed to simulate career path: ' + error.message });
  }
};

module.exports = {
  uploadResume,
  getJobMatch,
  simulateCareerPath
};