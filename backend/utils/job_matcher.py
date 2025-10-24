import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

class JobMatcher:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        
        # Sample job database (in a real application, this would be loaded from a database)
        self.jobs_database = [
            {
                "id": 1,
                "title": "Software Engineer",
                "description": "Develop and maintain web applications using Python, JavaScript, and React. Experience with REST APIs and database design required.",
                "required_skills": ["Python", "JavaScript", "React", "REST API", "SQL"]
            },
            {
                "id": 2,
                "title": "Data Scientist",
                "description": "Analyze large datasets to extract insights and build predictive models. Proficiency in Python, R, and machine learning frameworks required.",
                "required_skills": ["Python", "R", "Machine Learning", "Statistics", "Pandas"]
            },
            {
                "id": 3,
                "title": "DevOps Engineer",
                "description": "Manage cloud infrastructure and deployment pipelines. Experience with Docker, Kubernetes, and CI/CD tools required.",
                "required_skills": ["Docker", "Kubernetes", "CI/CD", "AWS", "Linux"]
            },
            {
                "id": 4,
                "title": "Frontend Developer",
                "description": "Build responsive user interfaces using modern JavaScript frameworks. Experience with React, Vue.js, or Angular required.",
                "required_skills": ["JavaScript", "React", "Vue.js", "HTML", "CSS"]
            },
            {
                "id": 5,
                "title": "Backend Developer",
                "description": "Design and implement server-side logic and databases. Experience with Node.js, Python, or Java required.",
                "required_skills": ["Node.js", "Python", "Java", "SQL", "REST API"]
            }
        ]
        
        # Prepare job descriptions for matching
        self._prepare_job_data()
    
    def _prepare_job_data(self):
        """Prepare job data for matching"""
        job_texts = []
        for job in self.jobs_database:
            # Combine title, description, and skills
            text = f"{job['title']} {job['description']} {' '.join(job['required_skills'])}"
            job_texts.append(self._preprocess_text(text))
        
        # Fit vectorizer on job texts
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def calculate_match_score(self, resume_skills, job_title):
        """Calculate match score between resume skills and a specific job"""
        # Find the job in database
        target_job = None
        for job in self.jobs_database:
            if job['title'].lower() == job_title.lower():
                target_job = job
                break
        
        if not target_job:
            return {"error": f"Job title '{job_title}' not found in database"}
        
        # Calculate skill overlap
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in target_job['required_skills']]
        
        matching_skills = set(resume_skills_lower) & set(job_skills_lower)
        missing_skills = set(job_skills_lower) - set(resume_skills_lower)
        
        # Calculate match percentage
        if len(job_skills_lower) > 0:
            match_percentage = (len(matching_skills) / len(job_skills_lower)) * 100
        else:
            match_percentage = 0
        
        return {
            "job_title": target_job['title'],
            "match_score": round(match_percentage, 2),
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "total_required_skills": len(job_skills_lower)
        }
    
    def get_job_recommendations(self, resume_skills, top_n=5):
        """Get job recommendations based on resume skills"""
        # Create a text representation of resume skills
        resume_text = ' '.join(resume_skills)
        resume_text_processed = self._preprocess_text(resume_text)
        
        # Vectorize resume text
        resume_vector = self.vectorizer.transform([resume_text_processed])
        
        # Calculate cosine similarity with all jobs
        similarities = cosine_similarity(resume_vector, self.job_vectors)
        
        # Get top recommendations
        top_indices = similarities.argsort()[0][-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            job = self.jobs_database[idx]
            similarity_score = similarities[0][idx]
            
            # Calculate skill overlap for this job
            resume_skills_lower = [skill.lower() for skill in resume_skills]
            job_skills_lower = [skill.lower() for skill in job['required_skills']]
            
            matching_skills = set(resume_skills_lower) & set(job_skills_lower)
            
            # Calculate match percentage
            if len(job_skills_lower) > 0:
                match_percentage = (len(matching_skills) / len(job_skills_lower)) * 100
            else:
                match_percentage = 0
            
            recommendations.append({
                "id": job["id"],
                "title": job["title"],
                "match_score": round(match_percentage, 2),
                "similarity_score": round(similarity_score * 100, 2),
                "matching_skills_count": len(matching_skills),
                "total_required_skills": len(job_skills_lower)
            })
        
        return recommendations

# Main execution when called from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python job_matcher.py <operation> [args]"}))
        sys.exit(1)
    
    operation = sys.argv[1]
    
    try:
        matcher = JobMatcher()
        
        if operation == "match" and len(sys.argv) >= 4:
            resume_skills = json.loads(sys.argv[2])
            job_title = sys.argv[3]
            result = matcher.calculate_match_score(resume_skills, job_title)
            print(json.dumps(result))
        elif operation == "recommend" and len(sys.argv) >= 3:
            resume_skills = json.loads(sys.argv[2])
            result = matcher.get_job_recommendations(resume_skills)
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "Invalid operation or arguments"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))