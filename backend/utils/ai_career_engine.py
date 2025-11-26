import json
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PyPDF2
import docx
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from utils.real_time_data import RealTimeDataFetcher

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class AICareerEngine:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        self.data_fetcher = RealTimeDataFetcher()
        
        # Fetch real-time job data instead of using sample data
        self.jobs_database = self._fetch_real_time_jobs()
        
        # Prepare job descriptions for matching
        self._prepare_job_data()
    
    def _fetch_real_time_jobs(self):
        """Fetch real-time job data from multiple sources"""
        raw_jobs = self.data_fetcher.fetch_all_jobs()
        
        # Convert raw job data to our format
        jobs_database = []
        for i, job in enumerate(raw_jobs):
            jobs_database.append({
                "id": job.get("id", i+1),
                "title": job.get("title", "Unknown Position"),
                "description": job.get("description", ""),
                "required_skills": job.get("skills", []),
                "company": job.get("company", "Unknown Company"),
                "location": job.get("location", "Unknown Location"),
                "url": job.get("url", ""),
                "created_at": job.get("created_at", "")
            })
        
        return jobs_database
    
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
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {e}")
    
    def extract_contact_info(self, text):
        """Extract contact information from text"""
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Phone pattern (simple pattern, can be improved)
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        
        # Name extraction (simplified approach)
        lines = text.split('\n')
        name = ""
        if lines:
            # Assume the first line with alphabetic characters is the name
            for line in lines[:3]:  # Check first 3 lines
                if line.strip() and any(c.isalpha() for c in line):
                    name = line.strip()
                    break
        
        return {
            "name": name,
            "emails": emails,
            "phones": phones
        }
    
    def extract_experience(self, text):
        """Extract experience information from text"""
        # Look for experience section
        experience_patterns = [
            r'(?i)work experience[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)experience[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)professional experience[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)employment[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text)
            if match:
                experience_text = match.group(1).strip()
                # Clean up the text
                experience_text = re.sub(r'\n\s*\n', '\n', experience_text)
                return experience_text
        
        # If no specific section found, return a portion of text that might contain experience
        lines = text.split('\n')
        experience_lines = []
        in_experience_section = False
        
        for line in lines:
            if re.search(r'(?i)(experience|employment|work)', line):
                in_experience_section = True
                continue
            elif in_experience_section and re.search(r'(?i)(education|skills|objective)', line):
                break
            elif in_experience_section:
                experience_lines.append(line)
        
        return '\n'.join(experience_lines).strip() if experience_lines else "Experience details would be extracted from resume"
    
    def extract_education(self, text):
        """Extract education information from text"""
        # Look for education section
        education_patterns = [
            r'(?i)education[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)academic background[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)qualifications[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)degrees[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)'
        ]
        
        for pattern in education_patterns:
            match = re.search(pattern, text)
            if match:
                education_text = match.group(1).strip()
                # Clean up the text
                education_text = re.sub(r'\n\s*\n', '\n', education_text)
                # Remove common section headers that might appear
                education_text = re.sub(r'(?i)^(education|academic background|qualifications|degrees)\s*:?', '', education_text, flags=re.MULTILINE)
                return education_text.strip()
        
        # If no specific section found, look for patterns that indicate education
        lines = text.split('\n')
        education_lines = []
        in_education_section = False
        education_section_started = False
        
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'bs', 'ms', 'ba', 'ma', 'b.sc', 'm.sc', 'gpa', 'graduated', 'diploma']
        
        for line in lines:
            # Check if this line starts an education section
            if re.search(r'(?i)(education|academic|qualifications|degrees)', line):
                in_education_section = True
                education_section_started = True
                continue
            # Check if this line ends the education section
            elif in_education_section and re.search(r'(?i)(experience|skills|work|employment|objective|summary|projects|references)', line):
                if education_lines and education_section_started:  # Only break if we've collected some education lines and started the section
                    break
                else:
                    in_education_section = False  # Reset and continue looking
                    continue
            # If we're in the education section or the line contains education keywords
            elif in_education_section or any(keyword in line.lower() for keyword in education_keywords):
                # Skip lines that are clearly section headers
                if not re.match(r'(?i)^(experience|skills|work|employment|objective|summary|projects|references)\s*:?', line.strip()):
                    education_lines.append(line)
        
        # If we have education lines, join them
        if education_lines:
            result = '\n'.join(education_lines).strip()
            return result
        
        # Fallback to the original method
        result = "Education details would be extracted from resume"
        return result if result != "Education details would be extracted from resume" else self._extract_education_fallback(text)
    
    def _extract_education_fallback(self, text):
        """Fallback method to extract education information"""
        # Look for common education patterns
        education_patterns = [
            r'(?i)(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.|b\.sc|m\.sc).*?(?:university|college|institute)',
            r'(?i)(university|college|institute).*?(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.|b\.sc|m\.sc)',
            r'(?i)(bs|ms|ba|ma|bsc|msc).*?(?:university|college|institute)',
            r'(?i)(university|college|institute).*?\d{4}.*?\d{4}'  # Institution with years
        ]
        
        found_education = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Reconstruct the full match
                if isinstance(match, tuple):
                    full_match = ' '.join(match).strip()
                else:
                    full_match = match.strip()
                found_education.append(full_match)
        
        return '\n'.join(list(set(found_education))) if found_education else "Education details would be extracted from resume"

    def extract_projects(self, text):
        """Extract project information from text"""
        # Look for projects section
        project_patterns = [
            r'(?i)projects[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)project experience[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)',
            r'(?i)key projects[:\n\s]*([\s\S]*?)(?=\n\n|\n[A-Z][a-z]+:|$)'
        ]
        
        for pattern in project_patterns:
            match = re.search(pattern, text)
            if match:
                projects_text = match.group(1).strip()
                # Clean up the text
                projects_text = re.sub(r'\n\s*\n', '\n\n', projects_text)  # Double newline for project separation
                # Remove common section headers that might appear
                projects_text = re.sub(r'(?i)^(projects|project experience|key projects)\s*:?', '', projects_text, flags=re.MULTILINE)
                return projects_text.strip()
        
        # If no specific section found, look for bullet points or numbered lists that might contain projects
        lines = text.split('\n')
        project_lines = []
        in_project_section = False
        project_section_started = False
        
        for line in lines:
            # Check if this line starts a project section
            if re.search(r'(?i)(projects|project experience|key projects)', line):
                in_project_section = True
                project_section_started = True
                continue
            # Check if this line ends the project section
            elif in_project_section and re.search(r'(?i)(education|skills|experience|work|employment)', line):
                if project_lines and project_section_started:  # Only break if we've collected some project lines and started the section
                    break
                else:
                    in_project_section = False  # Reset and continue looking
                    continue
            # If we're in the project section, collect lines
            elif in_project_section:
                # Skip lines that are clearly section headers
                if not re.match(r'(?i)^(education|skills|experience|work|employment|objective|summary|references)\s*:?', line.strip()):
                    project_lines.append(line)
            # Also look for bullet points or lines that might indicate projects even outside a projects section
            elif re.search(r'^\s*[-*•\d]+\s+', line) or re.search(r'(?i)(project|developed|built|created)', line):
                # Check if this looks like a project description
                if len(line.strip()) > 10:  # Only consider lines with substantial content
                    project_lines.append(line)
        
        result = '\n'.join(project_lines).strip() if project_lines else "Project details would be extracted from resume"
        return result

    def extract_skills(self, text):
        """Extract skills from text using NLP"""
        # Common tech skills (this should be expanded)
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'html', 'css', 'sql', 
            'mongodb', 'postgresql', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'flask', 'django', 'spring', 'angular', 'vue.js',
            'git', 'jenkins', 'ansible', 'terraform', 'linux', 'bash', 'c++', 'c#',
            'php', 'ruby', 'swift', 'kotlin', 'scala', 'go', 'rust', 'r', 'matlab',
            'excel', 'tableau', 'power bi', 'hadoop', 'spark', 'kafka', 'redis',
            'elasticsearch', 'nginx', 'apache', 'mysql', 'oracle', 'firebase',
            'graphql', 'rest api', 'microservices', 'devops', 'agile', 'scrum'
        ]
        
        # Process text with spaCy
        doc = nlp(text.lower())
        
        # Extract noun phrases that might be skills
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Combine with common skills
        all_potential_skills = common_skills + noun_phrases
        
        # Tokenize and clean the text
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        
        # Find matching skills
        found_skills = []
        for skill in all_potential_skills:
            if skill in text.lower() or skill in filtered_tokens:
                # Avoid duplicates and clean up
                skill_clean = skill.strip().title()
                # Filter out personal information and non-skill terms
                personal_info_terms = [
                    'university', 'college', 'school', 'name', 'email', 'phone', 'address', 
                    'street', 'city', 'state', 'zip', 'john', 'doe', 'example', 'gmail', 'com',
                    'senior', 'software', 'engineer', 'developer', 'manager', 'team', 'leader',
                    'experience', 'education', 'project', 'skill', 'bachelor', 'master', 'phd',
                    'bs', 'ms', 'ba', 'ma', 'b.sc', 'm.sc', 'technologies', 'technology',
                    'corporation', 'corp', 'inc', 'ltd', 'company', 'llc', 'international'
                ]
                
                # Check if the skill contains any personal info terms
                contains_personal_info = any(term in skill_clean.lower() for term in personal_info_terms)
                
                # Only add if it's a valid skill and not already added
                if (skill_clean not in found_skills and 
                    len(skill_clean) > 1 and 
                    not contains_personal_info and
                    skill_clean.replace(' ', '').isalnum()):
                    found_skills.append(skill_clean)
        
        return found_skills[:20]  # Limit to top 20 skills
    
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
        
        # Get salary data
        salary_data = self.data_fetcher.get_salary_data(job_title, target_job.get('location', ''))
        
        return {
            "job_title": target_job['title'],
            "company": target_job.get('company', ''),
            "location": target_job.get('location', ''),
            "url": target_job.get('url', ''),
            "match_score": round(match_percentage, 2),
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "total_required_skills": len(job_skills_lower),
            "salary_data": salary_data
        }
    
    def get_job_recommendations(self, resume_skills, top_n=5):
        """Get job recommendations based on resume skills"""
        # Refresh job data periodically
        self.jobs_database = self._fetch_real_time_jobs()
        self._prepare_job_data()
        
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
            
            # Get salary data
            salary_data = self.data_fetcher.get_salary_data(job['title'], job.get('location', ''))
            
            recommendations.append({
                "id": job["id"],
                "title": job["title"],
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "url": job.get("url", ""),
                "match_score": round(match_percentage, 2),
                "similarity_score": round(similarity_score * 100, 2),
                "matching_skills_count": len(matching_skills),
                "total_required_skills": len(job_skills_lower),
                "salary_data": salary_data
            })
        
        return recommendations
    
    def get_trending_skills(self):
        """Get trending skills from real-time data"""
        return self.data_fetcher.get_trending_skills()
    
    def predict_future_skills_ml(self, current_skills):
        """Predict future skills using ML model with clustering and trend analysis"""
        try:
            # Define comprehensive skill progression patterns based on industry data
            skill_progression_map = {
                'python': ['machine learning', 'data science', 'deep learning', 'ai engineering', 'flask', 'django'],
                'javascript': ['react', 'node.js', 'vue.js', 'angular', 'full stack development', 'express'],
                'java': ['spring', 'microservices', 'cloud architecture', 'devops', 'spring boot'],
                'react': ['react native', 'next.js', 'redux', 'front end architecture', 'gatsby'],
                'node.js': ['express', 'mongodb', 'microservices', 'api development', 'nestjs'],
                'machine learning': ['deep learning', 'neural networks', 'computer vision', 'nlp', 'tensorflow', 'pytorch'],
                'data science': ['big data', 'data engineering', 'ai', 'statistics', 'pandas', 'numpy'],
                'docker': ['kubernetes', 'containerization', 'devops', 'cloud', 'docker swarm'],
                'aws': ['cloud architecture', 'serverless', 'lambda', 'cloud security', 'ec2', 's3'],
                'sql': ['postgresql', 'mysql', 'database design', 'data modeling', 'mongodb'],
                'html': ['css', 'responsive design', 'front end development', 'sass'],
                'css': ['sass', 'bootstrap', 'tailwind', 'responsive design', 'material ui'],
                'tensorflow': ['pytorch', 'keras', 'deep learning', 'computer vision'],
                'pytorch': ['tensorflow', 'deep learning', 'nlp', 'computer vision'],
                'angular': ['angularjs', 'typescript', 'rxjs', 'ngrx'],
                'vue.js': ['nuxt.js', 'vuex', 'typescript', 'vue router'],
                'spring': ['spring boot', 'spring security', 'microservices', 'hibernate'],
                'kubernetes': ['helm', 'istio', 'prometheus', 'docker'],
                'react native': ['flutter', 'ionic', 'xamarin', 'expo'],
                'graphql': ['apollo', 'relay', 'prisma', 'nestjs']
            }
            
            # Get real-time trending skills
            trending_skills = self.get_trending_skills()
            
            # Create a TF-IDF vectorizer for skill similarity analysis
            all_skills = list(skill_progression_map.keys()) + [skill['skill'].lower() for skill in trending_skills]
            vectorizer = TfidfVectorizer()
            
            # Fit the vectorizer on all skills
            try:
                tfidf_matrix = vectorizer.fit_transform(all_skills)
            except ValueError:
                # Handle case where there are no skills
                tfidf_matrix = None
            
            predicted_skills = []
            
            # For each current skill, predict future skills
            for skill in current_skills:
                skill_lower = skill.lower()
                if skill_lower in skill_progression_map:
                    # Get related future skills
                    future_skills = skill_progression_map[skill_lower]
                    for future_skill in future_skills[:3]:  # Take top 3 related skills
                        # Find similar trending skills
                        similarity_score = 0.0
                        trend_info = None
                        
                        for trending_skill in trending_skills:
                            if trending_skill['skill'].lower() == future_skill.lower():
                                similarity_score = 0.8  # High similarity
                                trend_info = trending_skill
                                break
                        
                        predicted_skills.append({
                            'skill': future_skill.title(),
                            'trend': trend_info['trend'] if trend_info else 'increasing',
                            'growth_rate': trend_info['growth_rate'] if trend_info else round(25 + (hash(future_skill) % 20), 1),
                            'similarity_score': round(similarity_score, 2),
                            'description': f'Natural progression from {skill} expertise' + (f" - {trend_info['description']}" if trend_info else '')
                        })
            
            # Use clustering to identify skill groups and predict based on clusters
            if len(current_skills) > 1 and tfidf_matrix is not None:
                try:
                    # Apply K-means clustering to group similar skills
                    n_clusters = min(3, len(all_skills))
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                    clusters = kmeans.fit_predict(tfidf_matrix)
                    
                    # For each current skill, find cluster and suggest skills from same cluster
                    current_skill_indices = []
                    for skill in current_skills:
                        skill_lower = skill.lower()
                        if skill_lower in all_skills:
                            current_skill_indices.append(all_skills.index(skill_lower))
                    
                    # Find clusters of current skills
                    if current_skill_indices:
                        current_clusters = [clusters[i] for i in current_skill_indices]
                        # Get most common cluster
                        from collections import Counter
                        cluster_counts = Counter(current_clusters)
                        most_common_cluster = cluster_counts.most_common(1)[0][0]
                        
                        # Suggest skills from the same cluster that are not already known
                        cluster_indices = [i for i, cluster in enumerate(clusters) if cluster == most_common_cluster]
                        for idx in cluster_indices:
                            if all_skills[idx] not in [s.lower() for s in current_skills]:
                                skill_name = all_skills[idx].title()
                                # Check if this skill is trending
                                trend_info = None
                                for trending_skill in trending_skills:
                                    if trending_skill['skill'].lower() == all_skills[idx]:
                                        trend_info = trending_skill
                                        break
                                
                                predicted_skills.append({
                                    'skill': skill_name,
                                    'trend': trend_info['trend'] if trend_info else 'stable',
                                    'growth_rate': trend_info['growth_rate'] if trend_info else round(15 + (hash(all_skills[idx]) % 15), 1),
                                    'similarity_score': 0.7,
                                    'description': f'Recommended based on your skill cluster' + (f" - {trend_info['description']}" if trend_info else '')
                                })
                except Exception as cluster_error:
                    print(f"Clustering error: {cluster_error}")
            
            # Remove duplicates while preserving order
            seen_skills = set()
            unique_predictions = []
            for pred in predicted_skills:
                if pred['skill'].lower() not in seen_skills:
                    seen_skills.add(pred['skill'].lower())
                    unique_predictions.append(pred)
            
            # If we don't have enough predictions, add some general trending skills
            if len(unique_predictions) < 5:
                for skill in trending_skills:
                    if skill['skill'].lower() not in seen_skills:
                        unique_predictions.append(skill)
                        seen_skills.add(skill['skill'].lower())
                        if len(unique_predictions) >= 5:
                            break
            
            # Sort by growth rate and similarity score
            unique_predictions.sort(key=lambda x: (x.get('growth_rate', 0), x.get('similarity_score', 0)), reverse=True)
            
            return unique_predictions[:5]  # Return top 5 predictions
        except Exception as e:
            print(f"Error in ML prediction: {e}")
            # Fallback to trending skills
            return self.get_trending_skills()[:5]
    
    def predict_interview_questions(self, resume_data):
        """Predict interview questions based on resume data using ML and NLP"""
        try:
            # Extract key information from resume
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', '')
            education = resume_data.get('education', '')
            projects = resume_data.get('projects', '')
            
            # Define question templates based on different categories with difficulty levels
            technical_questions = [
                ("Explain the concept of {skill} and how you've applied it in your projects.", 'Medium'),
                ("What challenges have you faced while working with {skill} and how did you overcome them?", 'Hard'),
                ("Describe a project where you used {skill} and what you learned from it.", 'Medium'),
                ("How do you stay updated with the latest developments in {skill}?", 'Easy'),
                ("What are the best practices you follow when working with {skill}?", 'Medium'),
                ("Compare and contrast {skill} with similar technologies.", 'Hard'),
                ("How would you optimize performance when working with {skill}?", 'Hard')
            ]
            
            behavioral_questions = [
                ("Tell me about a time when you had to work under pressure. How did you handle it?", 'Medium'),
                ("Describe a situation where you had to solve a complex problem. What was your approach?", 'Hard'),
                ("Tell me about a time when you had to work with a difficult team member. How did you handle it?", 'Medium'),
                ("Describe a situation where you had to learn a new technology quickly. How did you approach it?", 'Medium'),
                ("Tell me about a time when you made a mistake. How did you handle it?", 'Medium'),
                ("Describe a time when you had to convince someone to see things your way.", 'Hard'),
                ("Tell me about a time when you had to make a difficult decision with incomplete information.", 'Hard')
            ]
            
            experience_questions = [
                ("Based on your experience at {company}, what was the most challenging project you worked on?", 'Hard'),
                ("What was your biggest achievement in your previous role?", 'Medium'),
                ("How did you contribute to your team's success at {company}?", 'Medium'),
                ("What did you learn from your experience working on {project}?", 'Medium'),
                ("How did you handle conflicts or disagreements in your previous role?", 'Hard'),
                ("Describe a time when you had to adapt to significant changes at work.", 'Medium'),
                ("What would you do differently in your previous role, knowing what you know now?", 'Hard')
            ]
            
            project_questions = [
                ("Tell me about the {project} project. What was your role and contribution?", 'Medium'),
                ("What challenges did you face while working on {project} and how did you overcome them?", 'Hard'),
                ("What technologies did you use in the {project} project and why?", 'Medium'),
                ("What would you do differently if you were to work on {project} again?", 'Hard'),
                ("How did the {project} project impact the business or organization?", 'Medium'),
                ("Describe the most technically challenging aspect of the {project} project.", 'Hard'),
                ("How did you ensure the quality and reliability of the {project} project?", 'Medium')
            ]
            
            # Generate questions based on resume data
            questions = []
            
            # Add technical questions based on skills with ML-based difficulty prediction
            for i, skill in enumerate(skills[:5]):  # Use top 5 skills
                # Determine difficulty based on skill complexity (simplified ML approach)
                complex_skills = ['machine learning', 'deep learning', 'neural networks', 'cloud architecture', 'devops']
                skill_difficulty = 'Hard' if skill.lower() in complex_skills else 'Medium'
                
                for template, base_difficulty in technical_questions[:4]:  # Use top 4 templates
                    question = template.replace('{skill}', skill)
                    # Adjust difficulty based on skill complexity
                    final_difficulty = skill_difficulty if base_difficulty == 'Medium' else base_difficulty
                    questions.append({
                        'id': len(questions) + 1,
                        'question': question,
                        'category': 'Technical',
                        'difficulty': final_difficulty,
                        'skill': skill,
                        'relevance_score': round(0.8 - (i * 0.1), 2)  # Higher relevance for top skills
                    })
            
            # Add behavioral questions with relevance scoring
            for i, (template, difficulty) in enumerate(behavioral_questions[:5]):
                questions.append({
                    'id': len(questions) + 1,
                    'question': template,
                    'category': 'Behavioral',
                    'difficulty': difficulty,
                    'relevance_score': round(0.7 - (i * 0.05), 2)
                })
            
            # Extract companies and projects from experience
            companies = re.findall(r'\b(?:at|with|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', experience, re.IGNORECASE)
            project_names = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Project|System|Platform|Application))', projects)
            
            # Add experience-based questions if experience data is available
            if companies:
                company = companies[0] if companies else 'your previous company'
                for i, (template, difficulty) in enumerate(experience_questions[:3]):
                    question = template.replace('{company}', company)
                    questions.append({
                        'id': len(questions) + 1,
                        'question': question,
                        'category': 'Experience',
                        'difficulty': difficulty,
                        'relevance_score': round(0.9 - (i * 0.1), 2)
                    })
            
            # Add project-based questions if projects data is available
            if project_names:
                for i, project_name in enumerate(project_names[:2]):  # Use top 2 projects
                    for template, difficulty in project_questions[:3]:  # Use top 3 templates
                        question = template.replace('{project}', project_name)
                        questions.append({
                            'id': len(questions) + 1,
                            'question': question,
                            'category': 'Project',
                            'difficulty': difficulty,
                            'project': project_name,
                            'relevance_score': round(0.85 - (i * 0.1), 2)
                        })
            
            # Use NLP to analyze experience text and generate custom questions
            if experience:
                # Process experience with spaCy
                doc = nlp(experience)
                
                # Extract key entities (organizations, dates, etc.)
                orgs = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE']]
                dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
                
                # Generate custom questions based on entities
                if orgs:
                    custom_questions = [
                        f"I see you worked at {orgs[0]}. What was the company culture like there?",
                        f"How did your role at {orgs[0]} prepare you for this position?"
                    ]
                    
                    for i, q in enumerate(custom_questions):
                        questions.append({
                            'id': len(questions) + 1,
                            'question': q,
                            'category': 'Experience',
                            'difficulty': 'Medium',
                            'relevance_score': 0.75
                        })
            
            # Ensure we have a good mix of questions
            if len(questions) < 10:
                # Add some general questions
                general_questions = [
                    ("Why do you want to work for our company?", 'Medium'),
                    ("Where do you see yourself in 5 years?", 'Medium'),
                    ("What are your strengths and weaknesses?", 'Medium'),
                    ("Why should we hire you?", 'Hard'),
                    ("What motivates you in your work?", 'Easy'),
                    ("How do you handle failure?", 'Medium'),
                    ("Describe your ideal work environment.", 'Easy')
                ]
                
                for i, (q, difficulty) in enumerate(general_questions):
                    questions.append({
                        'id': len(questions) + 1,
                        'question': q,
                        'category': 'General',
                        'difficulty': difficulty,
                        'relevance_score': round(0.5 - (i * 0.05), 2)
                    })
            
            # Sort questions by relevance score and then randomize within categories
            import random
            questions.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Group by category and shuffle within each group for variety
            categories = {}
            for q in questions:
                category = q['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(q)
            
            # Shuffle within each category
            for category_questions in categories.values():
                random.shuffle(category_questions)
            
            # Flatten the grouped questions
            shuffled_questions = []
            max_len = max(len(cat_questions) for cat_questions in categories.values()) if categories else 0
            
            for i in range(max_len):
                for category_questions in categories.values():
                    if i < len(category_questions):
                        shuffled_questions.append(category_questions[i])
            
            # Ensure unique questions
            seen_questions = set()
            unique_questions = []
            for q in shuffled_questions:
                if q['question'] not in seen_questions:
                    seen_questions.add(q['question'])
                    unique_questions.append(q)
            
            return unique_questions[:20]  # Return top 20 questions
            
        except Exception as e:
            print(f"Error in interview question prediction: {e}")
            # Fallback to generic questions
            fallback_questions = [
                {
                    'id': 1,
                    'question': 'Tell me about yourself.',
                    'category': 'General',
                    'difficulty': 'Easy',
                    'relevance_score': 1.0
                },
                {
                    'id': 2,
                    'question': 'What interests you about this position?',
                    'category': 'General',
                    'difficulty': 'Easy',
                    'relevance_score': 1.0
                },
                {
                    'id': 3,
                    'question': 'What are your strengths and weaknesses?',
                    'category': 'General',
                    'difficulty': 'Medium',
                    'relevance_score': 0.9
                }
            ]
            return fallback_questions

    def get_ai_mentor_response(self, user_query, resume_data):
        """Generate personalized career guidance based on user query and resume data"""
        try:
            # Extract key information from resume
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', '')
            education = resume_data.get('education', '')
            projects = resume_data.get('projects', '')
            
            # Get trending skills and job data for context
            trending_skills = self.get_trending_skills()
            job_data = self.jobs_database
            
            # Process user query with spaCy
            doc = nlp(user_query.lower())
            
            # Identify key entities and intent
            entities = [ent.text for ent in doc.ents]
            nouns = [token.text for token in doc if token.pos_ == 'NOUN']
            verbs = [token.text for token in doc if token.pos_ == 'VERB']
            
            # Keywords for different intents
            learning_keywords = ['learn', 'skill', 'course', 'study', 'education', 'improve', 'develop']
            project_keywords = ['project', 'build', 'create', 'develop', 'make']
            career_keywords = ['career', 'job', 'position', 'role', 'work', 'employment']
            resource_keywords = ['resource', 'youtube', 'coursera', 'udemy', 'tutorial', 'guide']
            
            # Determine intent based on keywords
            intent = 'general'
            if any(keyword in user_query.lower() for keyword in learning_keywords):
                intent = 'learning'
            elif any(keyword in user_query.lower() for keyword in project_keywords):
                intent = 'project'
            elif any(keyword in user_query.lower() for keyword in career_keywords):
                intent = 'career'
            elif any(keyword in user_query.lower() for keyword in resource_keywords):
                intent = 'resource'
            
            # Generate response based on intent
            response = ""
            
            if intent == 'learning':
                # Learning guidance
                response = self._generate_learning_guidance(user_query, skills, trending_skills)
            elif intent == 'project':
                # Project suggestions
                response = self._generate_project_suggestions(user_query, skills, projects)
            elif intent == 'career':
                # Career advice
                response = self._generate_career_advice(user_query, skills, experience, job_data)
            elif intent == 'resource':
                # Resource recommendations
                response = self._generate_resource_recommendations(user_query, skills)
            else:
                # General guidance
                response = self._generate_general_guidance(user_query, skills, experience, education, projects)
            
            return {
                "response": response,
                "intent": intent,
                "skills_analyzed": skills[:5],  # Top 5 skills
                "confidence": 0.85  # Confidence score (simplified)
            }
        except Exception as e:
            print(f"Error in AI mentor response generation: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now. Could you rephrase your question?",
                "intent": "error",
                "skills_analyzed": [],
                "confidence": 0.0
            }
    
    def _generate_learning_guidance(self, query, skills, trending_skills):
        """Generate learning guidance based on user query and skills"""
        # Extract skill from query
        query_skills = []
        for skill in skills:
            if skill.lower() in query.lower():
                query_skills.append(skill)
        
        # If no specific skill mentioned, suggest based on trending skills
        if not query_skills:
            # Find skills gap by comparing user skills with trending skills
            user_skill_names = [skill.lower() for skill in skills]
            trending_skill_names = [skill['skill'].lower() for skill in trending_skills]
            
            # Suggest trending skills not in user's skill set
            suggested_skills = []
            for trending_skill in trending_skills:
                if trending_skill['skill'].lower() not in user_skill_names:
                    suggested_skills.append(trending_skill)
            
            if suggested_skills:
                top_suggestion = suggested_skills[0]
                return f"Based on current market trends, I recommend learning {top_suggestion['skill']}. {top_suggestion['description']}. With a growth rate of {top_suggestion['growth_rate']}%, this skill is highly valuable right now."
            else:
                return "You have a strong skill set! To continue growing, consider deepening your expertise in your current skills or exploring adjacent technologies."
        else:
            # Provide specific learning guidance for mentioned skills
            skill = query_skills[0]
            return f"To improve your {skill} skills, I recommend: 1) Practice with real-world projects, 2) Take online courses from platforms like Coursera or Udemy, 3) Join relevant communities for knowledge sharing, 4) Contribute to open-source projects. Would you like specific resource recommendations for {skill}?"
    
    def _generate_project_suggestions(self, query, skills, projects):
        """Generate project suggestions based on user skills"""
        # Extract skill from query
        query_skills = []
        for skill in skills:
            if skill.lower() in query.lower():
                query_skills.append(skill)
        
        # Project templates based on skills
        project_templates = {
            'python': [
                "Build a web scraper to collect and analyze data from multiple sources",
                "Create a machine learning model to predict stock prices or weather patterns",
                "Develop a personal finance tracker with data visualization"
            ],
            'javascript': [
                "Build a real-time chat application using WebSockets",
                "Create a task management app with drag-and-drop functionality",
                "Develop a browser extension for productivity enhancement"
            ],
            'react': [
                "Build a social media dashboard with real-time updates",
                "Create an e-commerce platform with payment integration",
                "Develop a portfolio website with interactive animations"
            ],
            'data science': [
                "Analyze COVID-19 data to identify trends and patterns",
                "Build a recommendation system for movies or products",
                "Create a dashboard to visualize business metrics"
            ],
            'machine learning': [
                "Develop an image classification model for specific use cases",
                "Create a natural language processing tool for sentiment analysis",
                "Build a predictive maintenance system for industrial equipment"
            ]
        }
        
        # Find matching projects
        suggestions = []
        if query_skills:
            for skill in query_skills:
                skill_lower = skill.lower()
                for key, projects in project_templates.items():
                    if key in skill_lower or skill_lower in key:
                        suggestions.extend(projects)
        else:
            # Suggest projects based on user's top skills
            for skill in skills[:3]:  # Top 3 skills
                skill_lower = skill.lower()
                for key, projects in project_templates.items():
                    if key in skill_lower or skill_lower in key:
                        suggestions.extend(projects)
        
        if suggestions:
            return f"Here are some project ideas to prove your skills: 1) {suggestions[0]}, 2) {suggestions[1] if len(suggestions) > 1 else 'Build a personal website showcasing your work'}, 3) {suggestions[2] if len(suggestions) > 2 else 'Contribute to an open-source project'}. These projects will help demonstrate your practical abilities to potential employers."
        else:
            return "I'd be happy to suggest projects! Could you tell me more about what specific skills you'd like to showcase or what type of project interests you?"
    
    def _generate_career_advice(self, query, skills, experience, job_data):
        """Generate career advice based on user profile"""
        # Analyze skills match with job data
        skill_matches = {}
        for job in job_data[:10]:  # Top 10 jobs
            match_count = 0
            for skill in skills:
                if skill.lower() in ' '.join(job.get('required_skills', [])).lower():
                    match_count += 1
            if match_count > 0:
                skill_matches[job['title']] = match_count
        
        # Sort jobs by match count
        sorted_matches = sorted(skill_matches.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_matches:
            best_match = sorted_matches[0][0]
            match_count = sorted_matches[0][1]
            return f"Based on your skills, you're well-suited for roles like {best_match}. You match {match_count} required skills for this position. To strengthen your profile, consider gaining experience in the remaining required skills. Your current experience in '{experience[:100]}...' shows good foundation. Would you like specific advice on transitioning to {best_match}?"
        else:
            return "Your skill set is quite unique! To enhance your career prospects, consider specializing in a specific domain or acquiring skills that are in high demand. Based on your experience '{experience[:100]}...', you might want to explore roles that value diverse skill sets."
    
    def _generate_resource_recommendations(self, query, skills):
        """Generate learning resource recommendations"""
        # Extract skill from query
        query_skills = []
        for skill in skills:
            if skill.lower() in query.lower():
                query_skills.append(skill)
        
        # Resource recommendations by skill
        resources = {
            'python': [
                "Coursera: Python for Everybody by University of Michigan",
                "YouTube: Corey Schafer's Python Tutorials",
                "Book: 'Automate the Boring Stuff with Python'"
            ],
            'javascript': [
                "freeCodeCamp: JavaScript Algorithms and Data Structures",
                "YouTube: The Net Ninja's JavaScript Tutorials",
                "Book: 'Eloquent JavaScript' by Marijn Haverbeke"
            ],
            'react': [
                "Udemy: React - The Complete Guide by Maximilian Schwarzmüller",
                "YouTube: React Tutorial for Beginners by Programming with Mosh",
                "Official React Documentation and Tutorial"
            ],
            'data science': [
                "Coursera: IBM Data Science Professional Certificate",
                "Kaggle Learn Micro-Courses",
                "Book: 'Python for Data Analysis' by Wes McKinney"
            ],
            'machine learning': [
                "Coursera: Machine Learning by Andrew Ng",
                "fast.ai: Practical Deep Learning for Coders",
                "Book: 'Hands-On Machine Learning' by Aurélien Géron"
            ]
        }
        
        recommendations = []
        if query_skills:
            for skill in query_skills:
                skill_lower = skill.lower()
                for key, res in resources.items():
                    if key in skill_lower or skill_lower in key:
                        recommendations.extend(res)
        else:
            # General recommendations based on top skills
            for skill in skills[:3]:
                skill_lower = skill.lower()
                for key, res in resources.items():
                    if key in skill_lower or skill_lower in key:
                        recommendations.extend(res)
        
        if recommendations:
            return f"Here are some excellent resources: 1) {recommendations[0]}, 2) {recommendations[1] if len(recommendations) > 1 else 'Join relevant online communities'}, 3) {recommendations[2] if len(recommendations) > 2 else 'Practice on platforms like HackerRank or LeetCode'}. These will help you master the skills effectively."
        else:
            return "I recommend starting with foundational resources like freeCodeCamp, Coursera, or edX courses. These platforms offer comprehensive learning paths for various technologies. What specific skill would you like to focus on?"
    
    def _generate_general_guidance(self, query, skills, experience, education, projects):
        """Generate general career guidance"""
        # Create a comprehensive profile summary
        profile_summary = f"You have skills in {', '.join(skills[:5])} and experience in '{experience[:50]}...'. "
        
        # Provide general advice
        advice = [
            "Focus on building a strong portfolio that showcases your skills and projects.",
            "Network with professionals in your field through LinkedIn and industry events.",
            "Stay updated with industry trends by following relevant blogs and publications.",
            "Consider obtaining certifications in your area of expertise to validate your skills.",
            "Set specific, measurable career goals and create a plan to achieve them."
        ]
        
        return f"{profile_summary}Here's some general advice: {advice[0]} {advice[1]} {advice[2]} {advice[3]} {advice[4]} Would you like more specific guidance on any particular aspect of your career development?"

    def parse_resume(self, file_path, file_type):
        """Main function to parse resume"""
        # Extract text based on file type
        if file_type == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_type == 'docx':
            text = self.extract_text_from_docx(file_path)
        else:
            # For text files
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        if not text:
            return {"error": "Failed to extract text from file"}
        
        # Extract information
        contact_info = self.extract_contact_info(text)
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        education = self.extract_education(text)
        projects = self.extract_projects(text)
        
        return {
            "contact_info": contact_info,
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects
        }

# Main execution when called from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python ai_career_engine.py <operation> [args]"}))
        sys.exit(1)
    
    operation = sys.argv[1]
    
    try:
        engine = AICareerEngine()
        
        if operation == "parse" and len(sys.argv) >= 4:
            file_path = sys.argv[2]
            file_type = sys.argv[3]
            result = engine.parse_resume(file_path, file_type)
            print(json.dumps(result))
        elif operation == "match" and len(sys.argv) >= 4:
            resume_skills = json.loads(sys.argv[2])
            job_title = sys.argv[3]
            result = engine.calculate_match_score(resume_skills, job_title)
            print(json.dumps(result))
        elif operation == "recommend" and len(sys.argv) >= 3:
            resume_skills = json.loads(sys.argv[2])
            result = engine.get_job_recommendations(resume_skills)
            print(json.dumps(result))
        elif operation == "trending":
            result = engine.get_trending_skills()
            print(json.dumps(result))
        elif operation == "predict_future" and len(sys.argv) >= 3:
            current_skills = json.loads(sys.argv[2])
            result = engine.predict_future_skills_ml(current_skills)
            print(json.dumps(result))
        elif operation == "predict_questions" and len(sys.argv) >= 3:
            resume_data = json.loads(sys.argv[2])
            result = engine.predict_interview_questions(resume_data)
            print(json.dumps(result))
        elif operation == "ai_mentor" and len(sys.argv) >= 4:
            user_query = sys.argv[2]
            resume_data = json.loads(sys.argv[3])
            result = engine.get_ai_mentor_response(user_query, resume_data)
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "Invalid operation or arguments"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
