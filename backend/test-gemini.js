const axios = require('axios');

// Test Gemini API directly
const testGeminiAPI = async () => {
  try {
    const apiKey = process.env.GEMINI_API_KEY || 'AIzaSyBcZLRzxeeYffXS5gonBHz3J-SodNyrMpQ';
    console.log('Testing Gemini API with key:', apiKey.substring(0, 10) + '...');
    
    const prompt = "What are the best programming languages to learn in 2025?";
    const model = 'gemini-2.0-flash';
    
    const response = await axios.post(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
      contents: [{
        parts: [{
          text: prompt
        }]
      }]
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Success! Response:', response.data.candidates[0].content.parts[0].text.substring(0, 200) + '...');
  } catch (error) {
    console.error('Gemini API Error:', error.response?.data || error.message);
  }
};

testGeminiAPI();