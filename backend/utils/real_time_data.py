import json
import requests
import os
from datetime import datetime, timedelta
import pickle

class RealTimeDataFetcher:
    def __init__(self):
        # In a real implementation, these would be actual API keys
        # For demo purposes, we'll simulate the data
        self.github_jobs_url = "https://jobs.github.com/positions.json"
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID', 'demo')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY', 'demo')
        self.cache_file = 'job_data_cache.pkl'
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
    def fetch_github_jobs(self, description="", location=""):
        """
        Fetch jobs from GitHub Jobs API (simulated)
        In a real implementation, you would use:
        params = {'description': description, 'location': location}
        response = requests.get(self.github_jobs_url, params=params)
        return response.json()
        """
        # Simulated data for demonstration
        simulated_jobs = [
            {
                "id": "1",
                "title": "Senior Python Developer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "description": "We are looking for a Senior Python Developer with experience in Django and Flask frameworks. Must have knowledge of REST APIs and database design.",
                "skills": ["Python", "Django", "Flask", "REST API", "SQL", "PostgreSQL"],
                "url": "https://example.com/job/1",
                "created_at": "2023-05-15"
            },
            {
                "id": "2",
                "title": "Machine Learning Engineer",
                "company": "AI Innovations",
                "location": "New York, NY",
                "description": "Join our team to build cutting-edge machine learning models. Experience with TensorFlow, PyTorch, and cloud platforms required.",
                "skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "AWS", "Docker"],
                "url": "https://example.com/job/2",
                "created_at": "2023-05-10"
            },
            {
                "id": "3",
                "title": "Frontend Developer",
                "company": "Web Solutions",
                "location": "Remote",
                "description": "Create responsive web applications using React and modern JavaScript. Experience with state management and testing frameworks.",
                "skills": ["JavaScript", "React", "HTML", "CSS", "Redux", "Jest"],
                "url": "https://example.com/job/3",
                "created_at": "2023-05-12"
            },
            {
                "id": "4",
                "title": "DevOps Engineer",
                "company": "Cloud Systems",
                "location": "Austin, TX",
                "description": "Manage cloud infrastructure and CI/CD pipelines. Experience with Kubernetes, Docker, and monitoring tools required.",
                "skills": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Prometheus"],
                "url": "https://example.com/job/4",
                "created_at": "2023-05-14"
            },
            {
                "id": "5",
                "title": "Data Scientist",
                "company": "Analytics Pro",
                "location": "Boston, MA",
                "description": "Analyze complex datasets and build predictive models. Proficiency in Python, R, and statistical analysis tools required.",
                "skills": ["Python", "R", "Statistics", "Pandas", "Scikit-learn", "Tableau"],
                "url": "https://example.com/job/5",
                "created_at": "2023-05-11"
            }
        ]
        return simulated_jobs
    
    def fetch_adzuna_jobs(self, what="", where=""):
        """
        Fetch jobs from Adzuna API (simulated)
        In a real implementation, you would use:
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
        params = {
            'app_id': self.adzuna_app_id,
            'app_key': self.adzuna_app_key,
            'what': what,
            'where': where
        }
        response = requests.get(url, params=params)
        return response.json()
        """
        # Simulated data for demonstration
        simulated_jobs = [
            {
                "id": "6",
                "title": "Full Stack Developer",
                "company": "Startup Hub",
                "location": "Seattle, WA",
                "description": "Develop end-to-end web applications using modern technologies. Experience with Node.js, React, and MongoDB required.",
                "skills": ["JavaScript", "Node.js", "React", "MongoDB", "Express", "HTML/CSS"],
                "url": "https://example.com/job/6",
                "created_at": "2023-05-13"
            },
            {
                "id": "7",
                "title": "Cybersecurity Analyst",
                "company": "SecureTech",
                "location": "Washington, DC",
                "description": "Protect organizational assets from cyber threats. Experience with security frameworks and incident response required.",
                "skills": ["Cybersecurity", "SIEM", "Firewalls", "Incident Response", "CISSP", "Python"],
                "url": "https://example.com/job/7",
                "created_at": "2023-05-09"
            }
        ]
        return simulated_jobs
    
    def fetch_stackoverflow_jobs(self, search_term=""):
        """
        Fetch jobs from Stack Overflow Jobs API (simulated)
        """
        # Simulated data for demonstration
        simulated_jobs = [
            {
                "id": "8",
                "title": "Backend Engineer",
                "company": "DataSystems",
                "location": "Denver, CO",
                "description": "Design and implement scalable backend services. Experience with microservices architecture and cloud platforms.",
                "skills": ["Python", "Java", "Microservices", "AWS", "Docker", "Kafka"],
                "url": "https://example.com/job/8",
                "created_at": "2023-05-14"
            }
        ]
        return simulated_jobs
    
    def get_cached_data(self):
        """Load cached job data if available and not expired"""
        try:
            if os.path.exists(self.cache_file):
                cache_time = os.path.getmtime(self.cache_file)
                cache_datetime = datetime.fromtimestamp(cache_time)
                
                if datetime.now() - cache_datetime < self.cache_duration:
                    with open(self.cache_file, 'rb') as f:
                        return pickle.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
        return None
    
    def cache_data(self, data):
        """Cache job data to file"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_all_jobs(self, skills=None):
        """Fetch jobs from all sources and combine them"""
        # Check cache first
        cached_data = self.get_cached_data()
        if cached_data:
            return cached_data
        
        # If no cache or expired, fetch fresh data
        all_jobs = []
        
        try:
            # Fetch from different sources
            github_jobs = self.fetch_github_jobs()
            adzuna_jobs = self.fetch_adzuna_jobs()
            stackoverflow_jobs = self.fetch_stackoverflow_jobs()
            
            # Combine all jobs
            all_jobs.extend(github_jobs)
            all_jobs.extend(adzuna_jobs)
            all_jobs.extend(stackoverflow_jobs)
            
            # Cache the data
            self.cache_data(all_jobs)
            
            return all_jobs
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            # Return cached data if available, even if expired
            if cached_data:
                return cached_data
            # Return empty list if no data available
            return []
    
    def get_trending_skills(self):
        """Get trending skills based on job market demand"""
        # In a real implementation, this would analyze job postings
        # to identify skills that are increasingly in demand
        trending_skills = [
            {
                "skill": "Artificial Intelligence",
                "trend": "rapidly increasing",
                "growth_rate": 35.2,
                "description": "AI skills are in high demand across industries"
            },
            {
                "skill": "Cloud Architecture",
                "trend": "steadily increasing",
                "growth_rate": 28.7,
                "description": "Cloud skills continue to grow as more companies migrate to cloud platforms"
            },
            {
                "skill": "Cybersecurity",
                "trend": "rapidly increasing",
                "growth_rate": 32.1,
                "description": "Security skills are critical as cyber threats become more sophisticated"
            },
            {
                "skill": "Data Engineering",
                "trend": "steadily increasing",
                "growth_rate": 26.5,
                "description": "Data engineering skills are essential for managing big data pipelines"
            },
            {
                "skill": "DevOps",
                "trend": "stable",
                "growth_rate": 15.3,
                "description": "DevOps practices are now standard in software development"
            }
        ]
        return trending_skills
    
    def get_salary_data(self, job_title, location=""):
        """Get salary data for a specific job title"""
        # In a real implementation, this would fetch actual salary data
        # For now, we'll return simulated data based on job title
        base_salaries = {
            "Software Engineer": {"min": 80000, "max": 140000, "avg": 110000},
            "Data Scientist": {"min": 90000, "max": 160000, "avg": 125000},
            "DevOps Engineer": {"min": 85000, "max": 150000, "avg": 117500},
            "Frontend Developer": {"min": 70000, "max": 130000, "avg": 100000},
            "Backend Developer": {"min": 75000, "max": 135000, "avg": 105000},
            "Machine Learning Engineer": {"min": 100000, "max": 180000, "avg": 140000},
            "Full Stack Developer": {"min": 75000, "max": 140000, "avg": 107500},
            "Cybersecurity Analyst": {"min": 70000, "max": 130000, "avg": 100000},
            "Backend Engineer": {"min": 80000, "max": 145000, "avg": 112500}
        }
        
        # Adjust for location (simplified)
        location_multiplier = 1.0
        if "san francisco" in location.lower() or "new york" in location.lower():
            location_multiplier = 1.3
        elif "seattle" in location.lower() or "boston" in location.lower():
            location_multiplier = 1.2
        elif "austin" in location.lower() or "denver" in location.lower():
            location_multiplier = 1.1
            
        if job_title in base_salaries:
            salary_data = base_salaries[job_title]
            return {
                "min": int(salary_data["min"] * location_multiplier),
                "max": int(salary_data["max"] * location_multiplier),
                "avg": int(salary_data["avg"] * location_multiplier)
            }
        else:
            # Default salary range
            return {"min": 60000, "max": 120000, "avg": 90000}

# Example usage
if __name__ == "__main__":
    fetcher = RealTimeDataFetcher()
    
    # Fetch all jobs
    jobs = fetcher.fetch_all_jobs()
    print("Fetched jobs:", json.dumps(jobs, indent=2))
    
    # Get trending skills
    trending = fetcher.get_trending_skills()
    print("\nTrending skills:", json.dumps(trending, indent=2))
    
    # Get salary data
    salary = fetcher.get_salary_data("Software Engineer", "San Francisco")
    print("\nSalary data:", json.dumps(salary, indent=2))