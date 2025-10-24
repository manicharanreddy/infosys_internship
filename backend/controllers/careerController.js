const { getTrendingSkills, predictFutureSkillsML } = require('../utils/python_bridge');

// Predict future skills based on real-time trending data and ML
const predictFutureSkills = async (req, res) => {
  const { skills } = req.body;
  const skillsArray = skills.split(',').map(skill => skill.trim()).filter(skill => skill);
  
  try {
    // Use ML model for future skills prediction
    const mlPredictions = await predictFutureSkillsML(skillsArray);
    
    // Get real-time trending skills data as fallback
    const trendingSkills = await getTrendingSkills();
    
    // Combine ML predictions with trending skills
    let finalPredictions = [];
    if (mlPredictions && mlPredictions.length > 0) {
      finalPredictions = mlPredictions.slice(0, 5); // Top 5 ML predictions
    } else {
      // Fallback to trending skills if ML prediction fails
      const relevantPredictions = trendingSkills.filter(prediction => {
        return skillsArray.some(skill => 
          prediction.skill.toLowerCase().includes(skill.toLowerCase())
        );
      });
      finalPredictions = relevantPredictions.length > 0 ? relevantPredictions : trendingSkills.slice(0, 5);
    }
    
    const result = {
      currentSkills: skillsArray,
      predictions: finalPredictions
    };
    
    res.json(result);
  } catch (error) {
    console.error('Future skills prediction error:', error);
    // Fallback to mock data if real-time data fails
    const fallbackPredictions = [
      {
        skill: 'Quantum Computing',
        trend: 'rapidly increasing',
        growth_rate: 35.2,
        description: 'As quantum computers become more accessible, knowledge of quantum algorithms will be increasingly valuable.'
      },
      {
        skill: 'Edge AI',
        trend: 'rapidly increasing',
        growth_rate: 32.1,
        description: 'With the proliferation of IoT devices, running AI models on edge devices will become essential.'
      },
      {
        skill: 'Sustainable Tech',
        trend: 'steadily increasing',
        growth_rate: 28.7,
        description: 'Green software development and energy-efficient algorithms will become increasingly important.'
      }
    ];
    
    res.json({
      currentSkills: skillsArray,
      predictions: fallbackPredictions
    });
  }
};

// Check for bias in resume text using NLP
const checkBias = (req, res) => {
  const { resumeText } = req.body;
  const wordCount = resumeText.split(/\s+/).length;
  
  // More comprehensive bias detection
  const biasPatterns = [
    {
      category: 'Gendered Language',
      patterns: [
        { term: 'manpower', suggestion: 'workforce or personnel' },
        { term: 'chairman', suggestion: 'chairperson' },
        { term: 'fireman', suggestion: 'firefighter' },
        { term: 'policeman', suggestion: 'police officer' },
        { term: 'stewardess', suggestion: 'flight attendant' },
        { term: 'housewife', suggestion: 'homemaker' },
        { term: 'businessman', suggestion: 'business person' }
      ]
    },
    {
      category: 'Age-Based Language',
      patterns: [
        { term: 'young', suggestion: 'early in career' },
        { term: 'old', suggestion: 'experienced' },
        { term: 'recent graduate', suggestion: 'new graduate' }
      ]
    },
    {
      category: 'Cultural Bias',
      patterns: [
        { term: 'native speaker', suggestion: 'fluent speaker' },
        { term: 'American', suggestion: 'US-based (when referring to location)' }
      ]
    }
  ];
  
  const foundBiasIssues = [];
  let correctedText = resumeText;
  
  biasPatterns.forEach(category => {
    category.patterns.forEach(pattern => {
      const regex = new RegExp(`\\b${pattern.term}\\b`, 'gi');
      const matches = resumeText.match(regex);
      if (matches) {
        foundBiasIssues.push({
          category: category.category,
          term: pattern.term,
          suggestion: pattern.suggestion,
          count: matches.length
        });
        
        // Apply correction to text
        correctedText = correctedText.replace(regex, pattern.suggestion);
      }
    });
  });
  
  // Gendered pronouns check
  const masculinePronouns = (resumeText.match(/\b(he|him|his)\b/gi) || []).length;
  const femininePronouns = (resumeText.match(/\b(she|her|hers)\b/gi) || []).length;
  
  const result = {
    wordCount: wordCount,
    biasIssues: foundBiasIssues,
    genderPronouns: {
      masculine: masculinePronouns,
      feminine: femininePronouns
    },
    suggestions: foundBiasIssues.map(issue => 
      `Replace "${issue.term}" with "${issue.suggestion}" (${issue.count} occurrence${issue.count > 1 ? 's' : ''})`
    ),
    correctedText: correctedText
  };
  
  res.json(result);
};

// Generate portfolio from resume data using AI
const generatePortfolio = (req, res) => {
  const { name, email, phone, skills, experience, education, projects } = req.body;
  const skillsArray = skills.split(',').map(skill => skill.trim()).filter(skill => skill);
  
  // Parse projects from resume text
  let parsedProjects = [];
  
  if (projects && projects !== "Project details would be extracted from resume" && projects.trim().length > 10) {
    // Split projects by double newlines, bullet points, or numbered lists
    const projectSections = projects.split(/(?:\n\s*\n)|(?:\n\s*[-*•\d]+\.?\s+)/).filter(section => section.trim().length > 10);
    
    if (projectSections.length > 0) {
      projectSections.forEach((section, index) => {
        // Clean up the section
        const cleanSection = section.trim();
        
        // Split section into lines
        const lines = cleanSection.split('\n').filter(line => line.trim().length > 0);
        
        if (lines.length > 0) {
          // First line is typically the project title
          let title = lines[0].replace(/^[-\d.\s]+/, '').trim(); // Remove leading dashes/numbers
          
          // If the title is too long, it might be the description, so try to extract a better title
          if (title.length > 50) {
            // Look for project name patterns
            const projectTitleMatch = title.match(/(?:project|developed|built|created)?\s*:?\s*([A-Z][a-zA-Z0-9\s\-_]+?)(?:\s*-|\s*[-–—]|\s*$)/i);
            if (projectTitleMatch) {
              title = projectTitleMatch[1].trim();
            } else {
              // Just take the first 30 characters as title
              title = title.substring(0, 30) + '...';
            }
          }
          
          // Rest of the lines are the description
          const description = lines.slice(1).join(' ').trim() || lines[0].trim();
          
          // Extract technologies from skills that might be mentioned in the project
          const projectSkills = skillsArray.filter(skill => 
            section.toLowerCase().includes(skill.toLowerCase())
          );
          
          // If no skills found in project, use top 3 skills
          const technologies = projectSkills.length > 0 ? projectSkills : skillsArray.slice(0, 3);
          
          parsedProjects.push({
            title: title || `Project ${index + 1}`,
            description: description || section,
            technologies: technologies
          });
        }
      });
    }
    
    // If we still don't have projects, try a different approach
    if (parsedProjects.length === 0) {
      // Split by lines and look for project indicators
      const lines = projects.split('\n').filter(line => line.trim().length > 0);
      let currentProject = null;
      
      lines.forEach(line => {
        const cleanLine = line.trim();
        // Check if this line starts a new project (bullet point, numbered list, or capitalized start)
        if (/^[-*•\d]+\s+/i.test(cleanLine) || /^[A-Z]/.test(cleanLine)) {
          if (currentProject) {
            parsedProjects.push(currentProject);
          }
          
          // Extract title
          const title = cleanLine.replace(/^[-*•\d]+\s+/, '').substring(0, 50);
          currentProject = {
            title: title || 'Project',
            description: '',
            technologies: skillsArray.slice(0, 3)
          };
        } else if (currentProject) {
          // Add to current project description
          currentProject.description += ' ' + cleanLine;
        }
      });
      
      // Don't forget the last project
      if (currentProject) {
        parsedProjects.push(currentProject);
      }
    }
  }
  
  // If no projects were parsed, generate projects based on skills
  if (parsedProjects.length === 0) {
    const projectTemplates = [
      {
        title: 'E-Commerce Platform',
        description: 'A full-stack e-commerce solution built with modern web technologies',
        technologies: ['React', 'Node.js', 'MongoDB'],
        skillsMatch: ['JavaScript', 'React', 'Node.js', 'MongoDB']
      },
      {
        title: 'Task Management App',
        description: 'A collaborative task management application with real-time updates',
        technologies: ['Vue.js', 'Firebase', 'Express'],
        skillsMatch: ['JavaScript', 'Vue.js', 'Firebase', 'Express']
      },
      {
        title: 'Data Visualization Dashboard',
        description: 'Interactive dashboard for visualizing business metrics and KPIs',
        technologies: ['React', 'D3.js', 'Python'],
        skillsMatch: ['JavaScript', 'React', 'Python', 'Data Visualization']
      },
      {
        title: 'Mobile Application',
        description: 'Cross-platform mobile app for [industry] professionals',
        technologies: ['React Native', 'Redux', 'Firebase'],
        skillsMatch: ['JavaScript', 'React Native', 'Mobile Development']
      },
      {
        title: 'API Development',
        description: 'RESTful API service with authentication and data management',
        technologies: ['Node.js', 'Express', 'PostgreSQL'],
        skillsMatch: ['JavaScript', 'Node.js', 'API Development']
      }
    ];
    
    // Match projects to skills
    const matchedProjects = projectTemplates.filter(project => {
      const projectSkills = project.skillsMatch || [];
      return skillsArray.some(skill => 
        projectSkills.some(projSkill => 
          projSkill.toLowerCase().includes(skill.toLowerCase()) ||
          skill.toLowerCase().includes(projSkill.toLowerCase())
        )
      );
    });
    
    // If no matches, use first three projects
    parsedProjects = matchedProjects.length > 0 ? matchedProjects : projectTemplates.slice(0, 3);
  }
  
  // Generate a more personalized portfolio URL
  const sanitizedName = name.replace(/\s+/g, '-').toLowerCase().replace(/[^a-z0-9-]/g, '');
  // This is a demo URL - in a real implementation, this would link to an actual generated portfolio
  const portfolioUrl = `https://portfolio.example.com/${sanitizedName}-${Date.now()}`;
  
  const result = {
    name: name,
    email: email,
    phone: phone,
    skills: skillsArray,
    experience: experience,
    education: education,
    projects: parsedProjects,
    portfolioUrl: portfolioUrl,
    // Add a note that this is a demo implementation
    note: "This is a demo portfolio URL. In a production environment, this would link to an actual generated portfolio website."
  };
  
  res.json(result);
};

// Predict interview questions based on resume data
const predictInterviewQuestions = async (req, res) => {
  try {
    const resumeData = req.body;
    
    // Call Python script to predict interview questions
    const { predictInterviewQuestions } = require('../utils/python_bridge');
    const questions = await predictInterviewQuestions(resumeData);
    
    res.json({
      questions: questions
    });
  } catch (error) {
    console.error('Interview question prediction error:', error);
    res.status(500).json({ error: 'Failed to predict interview questions: ' + error.message });
  }
};

module.exports = {
  predictFutureSkills,
  checkBias,
  generatePortfolio,
  predictInterviewQuestions
};