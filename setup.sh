#!/bin/bash

echo "Setting up AI Career Platform..."

# Create uploads directory if it doesn't exist
mkdir -p backend/uploads

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
npm install
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Setup Python virtual environment and install dependencies
echo "Setting up Python environment..."
cd backend
if [ ! -f "ai_career_env/bin/python" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ai_career_env
fi

echo "Installing Python dependencies..."
ai_career_env/bin/pip install -r requirements.txt

echo "Downloading NLTK data..."
ai_career_env/bin/python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

cd ..

echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. In one terminal, run: cd backend && npm start"
echo "2. In another terminal, run: cd frontend && npm start"
echo ""
echo "The application will be available at http://localhost:3000"