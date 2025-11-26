const axios = require('axios');

// Test the AI Mentor endpoint
const testAIMentor = async () => {
  try {
    console.log('Testing AI Mentor functionality...');
    
    const response = await axios.post('http://localhost:5000/api/career/ai-mentor', {
      query: "What should I learn next to become a Data Scientist?",
      resumeData: {
        skills: ["Python", "SQL", "Excel", "Statistics"],
        experience: "2 years as a data analyst",
        education: "Bachelor's degree in Mathematics"
      }
    });
    
    console.log('AI Mentor Response:', response.data);
  } catch (error) {
    console.error('Error testing AI Mentor:', error.response ? error.response.data : error.message);
    
    // Let's also try a simpler test to see if the endpoint is working
    console.log('\nTrying a simple test...');
    try {
      const simpleResponse = await axios.post('http://localhost:5000/api/career/ai-mentor', {
        query: "Hello",
        resumeData: {
          skills: ["JavaScript"],
          experience: "1 year",
          education: "Computer Science"
        }
      });
      console.log('Simple test response:', simpleResponse.data);
    } catch (simpleError) {
      console.error('Simple test error:', simpleError.response ? simpleError.response.data : simpleError.message);
    }
  }
};

testAIMentor();