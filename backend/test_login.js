require('dotenv').config();
const mongoose = require('mongoose');
const User = require('./models/User');

mongoose.connect(process.env.MONGODB_URI)
  .then(async () => {
    console.log('Connected to MongoDB');
    
    // Find the user
    const user = await User.findOne({ email: 'manicharan9875@gmail.com' });
    if (user) {
      console.log('User found:', user.email);
      
      // Test password comparison
      const isMatch = await user.comparePassword('testpassword');
      console.log('Password match result:', isMatch);
    } else {
      console.log('User not found');
    }
    
    mongoose.connection.close();
  })
  .catch(err => {
    console.log('Error connecting to MongoDB:', err);
  });