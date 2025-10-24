import PyPDF2
import docx
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import json
import sys

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_contact_info(text):
    """Extract contact information from text"""
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Phone pattern (simple pattern, can be improved)
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    
    # Name extraction (simplified approach)
    # This is a basic approach and might not work perfectly for all cases
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

def extract_skills(text):
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
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Find matching skills
    found_skills = []
    for skill in all_potential_skills:
        if skill in text.lower() or skill in filtered_tokens:
            # Avoid duplicates and clean up
            skill_clean = skill.strip().title()
            if skill_clean not in found_skills:
                found_skills.append(skill_clean)
    
    return found_skills[:20]  # Limit to top 20 skills

def extract_experience(text):
    """Extract experience information"""
    # Look for experience section
    exp_keywords = ['experience', 'work history', 'employment', 'professional experience']
    
    # Find the start of experience section
    exp_start = -1
    for keyword in exp_keywords:
        pos = text.lower().find(keyword)
        if pos != -1:
            exp_start = pos
            break
    
    if exp_start == -1:
        return "No experience section found"
    
    # Look for education section as end marker
    edu_keywords = ['education', 'academic', 'university', 'college', 'degree']
    edu_start = len(text)
    for keyword in edu_keywords:
        pos = text.lower().find(keyword)
        if pos != -1 and pos > exp_start:
            edu_start = pos
            break
    
    # Extract experience section
    experience_text = text[exp_start:edu_start]
    
    # Extract job titles and companies (simplified)
    # This is a basic approach and would need more sophisticated NLP for better results
    sentences = nltk.sent_tokenize(experience_text)
    
    # Look for patterns like "Job Title at Company" or "Company - Job Title"
    jobs = []
    for sentence in sentences:
        # Simple pattern matching
        if ' at ' in sentence or ' - ' in sentence:
            jobs.append(sentence.strip())
    
    return {
        "section_text": experience_text[:500] + "..." if len(experience_text) > 500 else experience_text,
        "potential_jobs": jobs[:5]  # Limit to first 5
    }

def extract_education(text):
    """Extract education information"""
    # Look for education section
    edu_keywords = ['education', 'academic', 'university', 'college', 'degree', 'bachelor', 'master', 'phd']
    
    # Find the start of education section
    edu_start = -1
    for keyword in edu_keywords:
        pos = text.lower().find(keyword)
        if pos != -1:
            edu_start = pos
            break
    
    if edu_start == -1:
        return "No education section found"
    
    # Extract education section (until end of text or next major section)
    education_text = text[edu_start:]
    
    # Simple extraction of potential degrees
    degree_patterns = [
        r'\b(bachelor|master|phd|b\.?s\.?|m\.?s\.?|bachelor\'?s|master\'?s)\b',
        r'\b(degree|diploma|certificate)\b'
    ]
    
    degrees = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, education_text, re.IGNORECASE)
        degrees.extend(matches)
    
    return {
        "section_text": education_text[:500] + "..." if len(education_text) > 500 else education_text,
        "potential_degrees": list(set(degrees))  # Remove duplicates
    }

def parse_resume(file_path, file_type):
    """Main function to parse resume"""
    # Extract text based on file type
    if file_type == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        text = extract_text_from_docx(file_path)
    else:
        # For text files
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    
    if not text:
        return {"error": "Failed to extract text from file"}
    
    # Extract information
    contact_info = extract_contact_info(text)
    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)
    
    return {
        "contact_info": contact_info,
        "skills": skills,
        "experience": experience,
        "education": education
    }

# Main execution when called from command line
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python real_resume_parser.py <file_path> <file_type>"}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    file_type = sys.argv[2]
    
    try:
        result = parse_resume(file_path, file_type)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))