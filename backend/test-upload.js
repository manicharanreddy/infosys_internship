const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

const testUpload = async () => {
  try {
    const form = new FormData();
    form.append('resume', fs.createReadStream('test-resume.txt'));
    
    const response = await axios.post('http://localhost:5000/api/resume/upload', form, {
      headers: form.getHeaders()
    });
    
    console.log('Upload success:', response.data);
  } catch (error) {
    console.error('Upload error:', error.response ? error.response.data : error.message);
  }
};

testUpload();