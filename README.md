# AI Career Platform

An AI-powered career development platform that helps users optimize their resumes, find suitable job roles, and plan their career paths.

## Features

1. **Resume Upload & Parsing**
   - Upload resumes in PDF, DOC, or DOCX formats
   - Automatic parsing and extraction of key information

2. **Job Role Matching**
   - Enter a job role to see how well your resume matches
   - Get a match score and recommendations for improvement
   - Identify missing skills for your target role

3. **AI Career Path Simulator**
   - Shows future career outcomes based on skills you add/learn
   - Provides step-by-step career progression guidance

4. **Future Skill Predictor (2-5 Year Forecast)**
   - Predicts upcoming in-demand skills before they peak
   - Helps users stay ahead of industry trends

5. **Bias & Inclusivity Checker**
   - Ensures resumes are free of biased or non-inclusive language
   - Provides suggestions for improvement

6. **AI Portfolio Generator**
   - Converts resume information into a professional portfolio
   - Generates project ideas and portfolio website

## Technology Stack

### Frontend
- React.js
- CSS3 for styling
- Axios for API requests

### Backend
- Node.js with Express.js
- Multer for file uploads
- PDF-Parse for PDF processing
- Natural for NLP tasks

### AI/ML Components
- NLP models for resume parsing
- Machine learning models for skill matching
- Predictive models for future skills forecasting
- Python libraries: NLTK, spaCy, scikit-learn, pandas, numpy

## Project Structure

```
ai-career-platform/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── services/
│       ├── pages/
│       ├── App.js
│       └── index.js
└── backend/
    ├── controllers/
    ├── models/
    ├── routes/
    ├── services/
    ├── utils/
    └── server.js
```

## Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)
- Python 3.8 or higher

### Automated Setup (Recommended)
Run the setup script from the root directory:

**Windows:**
```
setup.bat
```

**Linux/Mac:**
```
chmod +x setup.sh
./setup.sh
```

### Manual Setup

#### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Set up Python virtual environment:
   ```
   python -m venv ai_career_env
   ```

4. Activate the virtual environment:
   
   **Windows:**
   ```
   ai_career_env\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```
   source ai_career_env/bin/activate
   ```

5. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Download required NLTK data:
   ```
   # While in the virtual environment
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```

7. Start the server:
   ```
   npm start
   ```
   or for development with auto-restart:
   ```
   npm run dev
   ```

#### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## API Endpoints

- `POST /api/resume/upload` - Upload and parse a resume
- `POST /api/job/match` - Get job matching score and recommendations
- `POST /api/career/simulate` - Simulate career path based on skills
- `POST /api/skills/predict` - Predict future in-demand skills
- `POST /api/bias/check` - Check resume for biased language
- `POST /api/portfolio/generate` - Generate portfolio from resume data

## Future Enhancements

1. Integration with job boards for real-time job recommendations
2. LinkedIn profile analysis and optimization
3. Salary prediction based on skills and experience
4. Interview preparation tools with AI-generated questions
5. Personalized learning path recommendations
6. Industry trend analysis and visualization

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.