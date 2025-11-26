const axios = require('axios');

async function test() {
  try {
    const response = await axios.post('http://localhost:5000/api/career/ai-mentor', {
      query: 'What skills should I learn for data science?',
      resumeData: {
        skills: ['Python', 'SQL']
      }
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
  }
}

test();