const axios = require('axios');

// Test the bias checker endpoint
const testBiasChecker = async () => {
  try {
    console.log('Testing bias checker...');
    
    const response = await axios.post('http://localhost:5000/api/career/check-bias', {
      resumeText: `John Doe
Software Engineer

Experience:
I started my career as a young programmer at a major tech company. As a freshman in college, I was the only foreigner in my class. I worked as a salesman for several years before becoming a software engineer.

Skills:
- Programming
- Problem solving
- Team leadership

I am a strong businessman who can lead any team to success. My manpower skills have helped me manage large projects.`
    });
    
    console.log('Bias Checker Response:', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error testing bias checker:', error.response ? error.response.data : error.message);
  }
};

testBiasChecker();