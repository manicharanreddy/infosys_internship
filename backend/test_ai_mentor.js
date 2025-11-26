const { getAIMentorResponse } = require('./utils/python_bridge');

async function test() {
  try {
    const result = await getAIMentorResponse('What skills should I learn for data science?', {skills: ['Python', 'SQL']});
    console.log('Result:', result);
  } catch (error) {
    console.error('Error:', error);
  }
}

test();