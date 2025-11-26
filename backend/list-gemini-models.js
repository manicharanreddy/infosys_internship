const axios = require('axios');

// List available Gemini models
const listGeminiModels = async () => {
  try {
    const apiKey = process.env.GEMINI_API_KEY || 'AIzaSyBcZLRzxeeYffXS5gonBHz3J-SodNyrMpQ';
    console.log('Listing Gemini models with key:', apiKey.substring(0, 10) + '...');
    
    const response = await axios.get(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`);
    
    console.log('Available models:');
    response.data.models.forEach(model => {
      console.log(`- ${model.name}: ${model.displayName || model.name}`);
    });
  } catch (error) {
    console.error('Error listing models:', error.response?.data || error.message);
  }
};

listGeminiModels();