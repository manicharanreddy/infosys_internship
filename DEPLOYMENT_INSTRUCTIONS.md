# AI Career Platform - Enhanced Version

This document provides instructions for setting up and running the enhanced AI Career Platform with authentication and dashboard features.

## Features Added

1. **Home Page** - Landing page with feature descriptions and "Get Started" button
2. **User Authentication** - Login and Registration pages with MongoDB integration
3. **User Dashboard** - Post-login dashboard with access to all platform tools
4. **Protected Routes** - Authentication required to access platform features

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- MongoDB (v4.4 or higher)
- Python 3.8 or higher

## Installation Instructions

### 1. Install MongoDB

#### Windows:
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the setup wizard
3. Start MongoDB service:
   ```
   net start MongoDB
   ```

#### macOS:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu):
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
```

### 2. Set up the Application

1. **Navigate to the project root directory:**
   ```bash
   cd ai-career-platform
   ```

2. **Run the setup script:**
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Update environment variables (if needed):**
   
   Edit `backend/.env` file to match your MongoDB configuration:
   ```env
   MONGODB_URI=mongodb://localhost:27017/ai-career-platform
   JWT_SECRET=your_jwt_secret_key_here
   PORT=5000
   ```

### 3. Start the Application

#### Backend Server:
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the server:
   ```bash
   npm start
   ```
   
   Or for development with auto-restart:
   ```bash
   npm run dev
   ```

#### Frontend Server:
1. Navigate to the frontend directory (in a new terminal):
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Access the Application

1. Open your browser and navigate to `http://localhost:3000`
2. You'll see the Home Page with feature descriptions
3. Click "Get Started" to go to the Login page
4. Register a new account or login with existing credentials
5. Access the dashboard and all platform features

## API Endpoints

### Authentication:
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (protected)

### Existing Platform Endpoints:
- `POST /api/resume/upload` - Upload and parse a resume
- `POST /api/job/match` - Get job matching score and recommendations
- `POST /api/career/simulate` - Simulate career path based on skills
- `POST /api/skills/predict` - Predict future in-demand skills
- `POST /api/bias/check` - Check resume for biased language
- `POST /api/portfolio/generate` - Generate portfolio from resume data

## Project Structure

```
ai-career-platform/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/          # Existing platform components
│       ├── pages/               # New pages (Home, Login, Register, Dashboard)
│       ├── services/
│       ├── styles/
│       ├── App.js               # Updated with routing
│       └── index.js             # Updated with BrowserRouter
├── backend/
│   ├── controllers/
│   │   ├── authController.js    # New authentication controller
│   │   ├── careerController.js
│   │   └── resumeController.js
│   ├── middleware/
│   │   └── authMiddleware.js    # New authentication middleware
│   ├── models/
│   │   └── User.js              # New User model
│   ├── routes/
│   │   ├── authRoutes.js        # New authentication routes
│   │   ├── careerRoutes.js
│   │   ├── resumeRoutes.js
│   │   └── trendingRoutes.js
│   ├── utils/
│   ├── .env                     # Environment variables
│   └── server.js                # Updated with MongoDB and auth routes
```

## Troubleshooting

### Common Issues:

1. **MongoDB Connection Error:**
   - Ensure MongoDB is running
   - Check the MONGODB_URI in `.env` file
   - Verify MongoDB is accessible on the specified port

2. **Port Conflicts:**
   - Change the PORT value in `.env` file
   - Default ports: Backend (5000), Frontend (3000)

3. **Dependency Issues:**
   - Delete `node_modules` folders in both frontend and backend
   - Run setup script again

4. **CORS Errors:**
   - Ensure both frontend and backend servers are running
   - Check CORS configuration in `backend/server.js`

## Security Notes

- JWT tokens are stored in localStorage (for development)
- In production, consider using HttpOnly cookies for better security
- Change the JWT_SECRET in `.env` to a strong, random secret
- Passwords are hashed using bcrypt before storage

## Future Enhancements

1. Password reset functionality
2. Email verification for new accounts
3. Social login options (Google, LinkedIn)
4. Profile management page
5. Persistent dashboard statistics
6. Role-based access control