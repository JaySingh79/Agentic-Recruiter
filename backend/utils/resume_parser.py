# import re
# import spacy
# from datetime import datetime, date
# from dateutil.relativedelta import relativedelta
# from dateutil.parser import parse
# from typing import List, Dict, Set, Tuple, Optional
# import warnings
# from collections import defaultdict
# import nltk
# from nltk.corpus import stopwords

# # Download required NLTK data
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords')

# class OptimizedResumeParser:
#     def __init__(self):
#         # Load spaCy model for NLP processing
#         try:
#             self.nlp = spacy.load("en_core_web_sm")
#         except OSError:
#             print("Installing spaCy model...")
#             import subprocess
#             subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
#             self.nlp = spacy.load("en_core_web_sm")
        
#         # Comprehensive technical skills database[1]
#         self.technical_skills = {
#             # Programming Languages
#             'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 
#             'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'c',
#             'objective-c', 'dart', 'lua', 'shell', 'bash', 'powershell',
            
#             # Web Technologies
#             'html', 'css', 'react', 'angular', 'vue.js', 'vue', 'node.js', 'express.js',
#             'django', 'flask', 'spring boot', 'spring', 'laravel', 'asp.net', 'jquery',
#             'bootstrap', 'tailwind', 'sass', 'less', 'webpack', 'babel', 'npm', 'yarn',
            
#             # Databases
#             'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'elasticsearch', 
#             'cassandra', 'oracle', 'sql server', 'sqlite', 'dynamodb', 'neo4j',
#             'mariadb', 'couchdb', 'influxdb', 'snowflake', 'bigquery',
            
#             # Cloud & DevOps
#             'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
#             'terraform', 'ansible', 'chef', 'puppet', 'gitlab ci', 'github actions',
#             'circleci', 'travis ci', 'helm', 'istio', 'prometheus', 'grafana',
            
#             # Data & Analytics
#             'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'spark',
#             'hadoop', 'kafka', 'airflow', 'tableau', 'power bi', 'looker',
#             'matplotlib', 'seaborn', 'plotly', 'jupyter', 'r studio',
            
#             # Mobile Development
#             'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic',
#             'cordova', 'phonegap', 'swift ui', 'jetpack compose',
            
#             # Tools & Platforms
#             'git', 'svn', 'mercurial', 'jira', 'confluence', 'slack', 'teams',
#             'figma', 'sketch', 'photoshop', 'illustrator', 'postman', 'insomnia',
#             'vs code', 'intellij', 'eclipse', 'pycharm', 'sublime text',
            
#             # Testing & QA
#             'selenium', 'cypress', 'jest', 'mocha', 'jasmine', 'pytest', 'junit',
#             'testng', 'cucumber', 'postman', 'rest assured', 'appium',
            
#             # Additional Technologies
#             'microservices', 'restful', 'graphql', 'grpc', 'oauth', 'jwt',
#             'blockchain', 'ethereum', 'solidity', 'machine learning', 'deep learning',
#             'nlp', 'computer vision', 'api', 'rest', 'soap', 'json', 'xml'
#         }
        
#         # Acronym mapping for skill normalization[1]
#         self.skill_mapping = {
#             'js': 'javascript', 'ts': 'typescript', 'py': 'python',
#             'react.js': 'react', 'vue.js': 'vue', 'postgres': 'postgresql',
#             'mongo': 'mongodb', 'k8s': 'kubernetes', 'tf': 'tensorflow',
#             'sklearn': 'scikit-learn', 'ml': 'machine learning', 'dl': 'deep learning',
#             'ai': 'artificial intelligence', 'cv': 'computer vision',
#             'nlp': 'natural language processing', 'db': 'database'
#         }
        
#         # Experience-related patterns
#         self.experience_patterns = [
#             # Explicit experience statements[3]
#             r'(?:total\s+)?(?:experience|exp)(?:\s+of)?\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
#             r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:of\s+)?(?:experience|exp)',
#             r'(?:over|more than|above)\s+(\d+(?:\.\d+)?)\s*years?\s+(?:of\s+)?(?:experience|exp)',
            
#             # Date range patterns[6]
#             r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\s*(?:to|[\-–])\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
#             r'(\d{1,2}[\/\-]\d{2,4})\s*(?:to|[\-–])\s*(\d{1,2}[\/\-]\d{2,4})',
#             r'(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})\s*(?:to|[\-–])\s*(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})',
#             r'(\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4})\s*(?:to|[\-–])\s*(\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4})',
#             r'(\d{2,4})\s*(?:to|[\-–])\s*(\d{2,4})',
            
#             # Present/Current patterns
#             r'(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})\s*(?:to|[\-–])\s*(?:present|current|now)',
#             r'(\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4})\s*(?:to|[\-–])\s*(?:present|current|now)',
#             r'(\d{1,2}[\/\-]\d{2,4})\s*(?:to|[\-–])\s*(?:present|current|now)',
#             r'(\d{2,4})\s*(?:to|[\-–])\s*(?:present|current|now)'
#         ]
        
#         self.stop_words = set(stopwords.words('english'))
        
#     def extract_technical_skills(self, resume_text: str) -> List[str]:
#         """Extract technical skills using multiple advanced techniques[1]"""
#         skills_found = set()
#         text_lower = resume_text.lower()
        
#         # Method 1: Direct skill matching with word boundaries
#         for skill in self.technical_skills:
#             if re.search(rf'\b{re.escape(skill)}\b', text_lower):
#                 skills_found.add(skill)
        
#         # Method 2: Context-based skill extraction
#         skill_contexts = [
#             r'(?:skills?|technologies?|tools?|frameworks?|languages?)[:\-]?\s*([^.]{1,200})',
#             r'(?:proficient|experienced|expertise|familiar)\s+(?:with|in)\s+([^.]{1,100})',
#             r'(?:knowledge|experience)\s+(?:of|in|with)\s+([^.]{1,100})',
#             r'(?:using|worked with|utilized)\s+([^.]{1,100})'
#         ]
        
#         for pattern in skill_contexts:
#             matches = re.finditer(pattern, text_lower, re.IGNORECASE)
#             for match in matches:
#                 context = match.group(1)
#                 # Extract potential skills from context
#                 potential_skills = re.findall(r'\b[a-z]+(?:\.[a-z]+)*\b', context)
#                 for skill in potential_skills:
#                     normalized = self.skill_mapping.get(skill, skill)
#                     if normalized in self.technical_skills:
#                         skills_found.add(normalized)
        
#         # Method 3: NLP-based extraction
#         doc = self.nlp(resume_text)
#         for token in doc:
#             if token.text.lower() in self.technical_skills:
#                 skills_found.add(token.text.lower())
        
#         # Method 4: Acronym handling[1]
#         for acronym, full_form in self.skill_mapping.items():
#             if re.search(rf'\b{re.escape(acronym)}\b', text_lower):
#                 if full_form in self.technical_skills:
#                     skills_found.add(full_form)
        
#         return sorted(list(skills_found))
    
#     def parse_date(self, date_str: str) -> Optional[date]:
#         """Parse various date formats"""
#         if not date_str:
#             return None
        
#         date_str = date_str.strip().lower()
        
#         # Handle "present", "current", "now"
#         if any(word in date_str for word in ['present', 'current', 'now']):
#             return date.today()
        
#         try:
#             # Try to parse the date
#             parsed_date = parse(date_str, fuzzy=True)
#             return parsed_date.date()
#         except:
#             # Try manual parsing for various formats
#             patterns = [
#                 r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})',  # MM/DD/YYYY or DD/MM/YYYY
#                 r'(\d{1,2})[\/\-](\d{2,4})',  # MM/YYYY
#                 r'(\d{2,4})'  # YYYY
#             ]
            
#             for pattern in patterns:
#                 match = re.search(pattern, date_str)
#                 if match:
#                     try:
#                         if len(match.groups()) == 3:
#                             month, day, year = match.groups()
#                             year = int(year)
#                             if year < 50:
#                                 year += 2000
#                             elif year < 100:
#                                 year += 1900
#                             return date(year, int(month), int(day))
#                         elif len(match.groups()) == 2:
#                             month, year = match.groups()
#                             year = int(year)
#                             if year < 50:
#                                 year += 2000
#                             elif year < 100:
#                                 year += 1900
#                             return date(year, int(month), 1)
#                         else:
#                             year = int(match.group(1))
#                             if year < 50:
#                                 year += 2000
#                             elif year < 100:
#                                 year += 1900
#                             return date(year, 1, 1)
#                     except:
#                         continue
        
#         return None
    
#     def extract_experience_years(self, resume_text: str) -> Dict[str, float]:
#         """Extract years of experience using advanced techniques[3]"""
#         experience_data = {
#             'total_calculated': 0.0,
#             'total_stated': 0.0,
#             'total_experience': 0.0,
#             'job_periods': []
#         }
        
#         # Method 1: Extract explicitly stated experience[3]
#         explicit_patterns = [
#             r'(?:total\s+)?(?:experience|exp)(?:\s+of)?\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
#             r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:of\s+)?(?:experience|exp)',
#             r'(?:over|more than|above)\s+(\d+(?:\.\d+)?)\s*years?\s+(?:of\s+)?(?:experience|exp)'
#         ]
        
#         for pattern in explicit_patterns:
#             matches = re.finditer(pattern, resume_text, re.IGNORECASE)
#             for match in matches:
#                 years = float(match.group(1))
#                 experience_data['total_stated'] = max(experience_data['total_stated'], years)
        
#         # Method 2: Calculate from job periods[3]
#         job_periods = []
        
#         # Find all date ranges in the resume
#         for pattern in self.experience_patterns[3:]:  # Skip explicit experience patterns
#             matches = re.finditer(pattern, resume_text, re.IGNORECASE)
#             for match in matches:
#                 if len(match.groups()) >= 2:
#                     start_date = self.parse_date(match.group(1))
#                     end_date = self.parse_date(match.group(2))
                    
#                     if start_date and end_date:
#                         # Ensure start_date is before end_date
#                         if start_date > end_date:
#                             start_date, end_date = end_date, start_date
                        
#                         job_periods.append((start_date, end_date))
        
#         # Calculate total experience from job periods[3]
#         if job_periods:
#             # Sort job periods by start date
#             job_periods.sort(key=lambda x: x[0])
            
#             # Handle overlapping periods
#             merged_periods = []
#             for start, end in job_periods:
#                 if not merged_periods or merged_periods[-1][1] < start:
#                     merged_periods.append((start, end))
#                 else:
#                     # Merge overlapping periods
#                     merged_periods[-1] = (merged_periods[-1][0], max(merged_periods[-1][1], end))
            
#             # Calculate total months
#             total_months = 0
#             for start, end in merged_periods:
#                 delta = relativedelta(end, start)
#                 months = delta.years * 12 + delta.months
#                 total_months += months
            
#             experience_data['total_calculated'] = round(total_months / 12, 2)
#             experience_data['job_periods'] = merged_periods
        
#         # Take the higher value between stated and calculated[3]
#         experience_data['total_experience'] = max(
#             experience_data['total_stated'],
#             experience_data['total_calculated']
#         )
        
#         return experience_data
    
#     def parse_resume(self, resume_text: str) -> Dict:
#         """
#         Main function to parse resume and extract skills and experience
        
#         Args:
#             resume_text (str): Raw resume text
            
#         Returns:
#             Dict: Parsed resume data with skills and experience
#         """
#         if not resume_text or not isinstance(resume_text, str):
#             return {
#                 'technical_skills': [],
#                 'experience': {
#                     'total_experience': 0.0,
#                     'total_calculated': 0.0,
#                     'total_stated': 0.0,
#                     'job_periods': []
#                 }
#             }
        
#         # Extract technical skills
#         technical_skills = self.extract_technical_skills(resume_text)
        
#         # Extract experience
#         experience_data = self.extract_experience_years(resume_text)
        
#         return {
#             'technical_skills': technical_skills,
#             'experience': experience_data,
#             'skills_count': len(technical_skills),
#             'processing_summary': {
#                 'skills_extraction_method': 'Multi-layer NLP + Context + Acronym mapping',
#                 'experience_calculation_method': 'Date parsing + Overlap handling + Explicit statement comparison'
#             }
#         }

# # Usage function
# def parse_resume_comprehensive(resume_text: str) -> Dict:
#     """
#     Ultra-optimized resume parser for technical skills and experience extraction
    
#     Args:
#         resume_text (str): Raw resume text
        
#     Returns:
#         Dict: Comprehensive parsing results
#     """
#     parser = OptimizedResumeParser()
#     return parser.parse_resume(resume_text)

# # Example usage
# if __name__ == "__main__":
#     sample_resume = """
#     John Doe
#     Software Engineer
#     Email: john.doe@example.com
    
#     EXPERIENCE:
#     Total Experience: 5.5 years
    
#     Senior Software Engineer | ABC Tech | March 2020 - Present
#     - Developed web applications using React, Node.js, and MongoDB
#     - Implemented CI/CD pipelines with Docker and Kubernetes
#     - Led team of 5 developers using Agile methodologies
    
#     Software Developer | XYZ Corp | January 2018 - February 2020
#     - Built REST APIs using Python Django and PostgreSQL
#     - Utilized AWS services including EC2, S3, and RDS
#     - Implemented automated testing with pytest and selenium
    
#     TECHNICAL SKILLS:
#     Programming Languages: Python, JavaScript, TypeScript, Java
#     Frameworks: React, Angular, Django, Flask, Spring Boot
#     Databases: PostgreSQL, MongoDB, Redis, MySQL
#     Cloud: AWS, Azure, Docker, Kubernetes
#     Tools: Git, Jenkins, Jira, Postman
#     """
    
#     result = parse_resume_comprehensive(sample_resume)
#     print("Technical Skills Found:", result['technical_skills'])
#     print("Total Experience:", result['experience']['total_experience'], "years")
#     print("Calculated Experience:", result['experience']['total_calculated'], "years")
#     print("Stated Experience:", result['experience']['total_stated'], "years")
#     print("Number of Skills:", result['skills_count'])














import re
import spacy
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import dateutil.parser as date_parser
from typing import List, Dict, Set, Tuple, Optional
import warnings
from collections import defaultdict, Counter

class AccurateResumeParser:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Technical skills database
        self.technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'mysql', 'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'docker',
            'kubernetes', 'jenkins', 'git', 'tensorflow', 'pytorch', 'pandas'
        }
        
        # Experience section keywords
        self.experience_keywords = [
            'experience', 'work experience', 'professional experience',
            'employment', 'career', 'work history', 'professional history'
        ]
        
        # Job title patterns
        self.job_title_patterns = [
            r'(?:senior|lead|principal|staff|chief)\s+(?:software|data|machine learning|ml|ai|backend|frontend|full stack|devops)\s+(?:engineer|developer|scientist|architect)',
            r'(?:software|data|machine learning|ml|ai|backend|frontend|full stack|devops)\s+(?:engineer|developer|scientist|architect)',
            r'(?:senior|lead|principal|staff|chief)\s+(?:analyst|consultant|manager|director)',
            r'(?:project|product|technical)\s+(?:manager|lead|coordinator)',
            r'(?:intern|trainee|associate|junior)\s+(?:engineer|developer|analyst)'
        ]
        
        # Month name mapping
        self.month_mapping = {
            'january': '01', 'jan': '01', 'february': '02', 'feb': '02',
            'march': '03', 'mar': '03', 'april': '04', 'apr': '04',
            'may': '05', 'june': '06', 'jun': '06', 'july': '07', 'jul': '07',
            'august': '08', 'aug': '08', 'september': '09', 'sep': '09',
            'october': '10', 'oct': '10', 'november': '11', 'nov': '11',
            'december': '12', 'dec': '12'
        }
    
    def extract_experience_section(self, resume_text: str) -> str:
        """Extract the experience section from resume"""
        lines = resume_text.split('\n')
        experience_section = []
        in_experience = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this line starts experience section
            if any(keyword in line_lower for keyword in self.experience_keywords):
                in_experience = True
                continue
            
            # Check if we've moved to a new section
            if in_experience and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                # Check if this is a new major section
                if any(section in line_lower for section in ['education', 'skills', 'projects', 'certifications', 'achievements']):
                    break
            
            if in_experience:
                experience_section.append(line)
        
        return '\n'.join(experience_section)
    
    def parse_date_flexible(self, date_str: str) -> Optional[date]:
        """More robust date parsing"""
        if not date_str:
            return None
        
        date_str = date_str.lower().strip()
        
        # Handle present/current
        if any(word in date_str for word in ['present', 'current', 'now', 'ongoing']):
            return date.today()
        
        # Clean the date string
        date_str = re.sub(r'[^\w\s/-]', '', date_str)
        
        # Try various date formats
        date_patterns = [
            r'(\w+)\s+(\d{4})',  # Month Year
            r'(\d{1,2})[/-](\d{4})',  # MM/YYYY
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',  # MM/DD/YYYY
            r'(\d{4})',  # Just year
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    if len(match.groups()) == 2:
                        part1, part2 = match.groups()
                        # Check if first part is month name
                        if part1 in self.month_mapping:
                            month = self.month_mapping[part1]
                            year = int(part2)
                            return date(year, int(month), 1)
                        else:
                            # Assume MM/YYYY format
                            return date(int(part2), int(part1), 1)
                    elif len(match.groups()) == 3:
                        # MM/DD/YYYY format
                        month, day, year = match.groups()
                        year = int(year)
                        if year < 50:
                            year += 2000
                        elif year < 100:
                            year += 1900
                        return date(year, int(month), int(day))
                    else:
                        # Just year
                        year = int(match.group(1))
                        return date(year, 1, 1)
                except:
                    continue
        
        # Fallback to dateutil parser
        try:
            parsed = date_parser.parse(date_str, fuzzy=True)
            return parsed.date()
        except:
            return None
    
    def extract_job_entries(self, experience_text: str) -> List[Dict]:
        """Extract individual job entries with better accuracy"""
        job_entries = []
        
        # Split into potential job blocks
        lines = experience_text.split('\n')
        current_job = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line contains a job title and company
            # Pattern: Job Title | Company | Date Range
            # Pattern: Job Title at Company (Date Range)
            # Pattern: Job Title - Company - Date Range
            
            job_patterns = [
                r'(.+?)\s*[\|@]\s*(.+?)\s*[\|@-]\s*(.+)',
                r'(.+?)\s+at\s+(.+?)\s*[\(\[](.+?)[\)\]]',
                r'(.+?)\s*-\s*(.+?)\s*-\s*(.+)',
                r'(.+?)\s*,\s*(.+?)\s*[\(\[](.+?)[\)\]]'
            ]
            
            job_match = None
            for pattern in job_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    job_match = match
                    break
            
            if job_match:
                job_title = job_match.group(1).strip()
                company = job_match.group(2).strip()
                date_range = job_match.group(3).strip()
                
                # Extract start and end dates
                date_parts = re.split(r'\s*(?:to|[-–])\s*', date_range, maxsplit=1)
                
                if len(date_parts) == 2:
                    start_date = self.parse_date_flexible(date_parts[0])
                    end_date = self.parse_date_flexible(date_parts[1])
                    
                    if start_date:
                        job_entries.append({
                            'title': job_title,
                            'company': company,
                            'start_date': start_date,
                            'end_date': end_date or date.today(),
                            'raw_text': line
                        })
        
        return job_entries
    
    def calculate_total_experience(self, job_entries: List[Dict]) -> Dict:
        """Calculate total experience with improved accuracy"""
        if not job_entries:
            return {'total_months': 0, 'total_years': 0, 'details': []}
        
        # Sort jobs by start date
        sorted_jobs = sorted(job_entries, key=lambda x: x['start_date'])
        
        # Calculate experience for each job
        job_details = []
        total_months = 0
        
        for job in sorted_jobs:
            start_date = job['start_date']
            end_date = job['end_date']
            
            # Calculate months for this job
            delta = relativedelta(end_date, start_date)
            months = delta.years * 12 + delta.months
            
            # Add partial month if days > 15
            if delta.days > 15:
                months += 1
            
            job_details.append({
                'title': job['title'],
                'company': job['company'],
                'start_date': start_date.strftime('%Y-%m'),
                'end_date': end_date.strftime('%Y-%m'),
                'duration_months': months,
                'duration_years': round(months / 12, 1)
            })
            
            total_months += months
        
        # Handle overlapping periods (more conservative approach)
        # Remove overlaps by taking the maximum end date for overlapping periods
        merged_periods = []
        for job in sorted_jobs:
            start = job['start_date']
            end = job['end_date']
            
            # Check for overlaps with existing periods
            overlapping = False
            for i, period in enumerate(merged_periods):
                if start <= period[1] and end >= period[0]:
                    # Merge overlapping periods
                    merged_periods[i] = (min(start, period[0]), max(end, period[1]))
                    overlapping = True
                    break
            
            if not overlapping:
                merged_periods.append((start, end))
        
        # Recalculate total from merged periods
        adjusted_total_months = 0
        for start, end in merged_periods:
            delta = relativedelta(end, start)
            months = delta.years * 12 + delta.months
            if delta.days > 15:
                months += 1
            adjusted_total_months += months
        
        return {
            'total_months': adjusted_total_months,
            'total_years': round(adjusted_total_months / 12, 1),
            'raw_total_months': total_months,
            'raw_total_years': round(total_months / 12, 1),
            'job_count': len(job_entries),
            'details': job_details,
            'merged_periods': [(s.strftime('%Y-%m'), e.strftime('%Y-%m')) for s, e in merged_periods]
        }
    
    def extract_stated_experience(self, resume_text: str) -> Optional[float]:
        """Extract explicitly stated total experience"""
        patterns = [
            r'(?:total|overall)\s+(?:experience|exp)[\s:]*(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:of\s+)?(?:total|overall|professional)\s+(?:experience|exp)',
            r'(?:experience|exp)[\s:]*(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:experience|exp)'
        ]
        
        max_stated = 0
        for pattern in patterns:
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                try:
                    years = float(match.group(1))
                    max_stated = max(max_stated, years)
                except:
                    continue
        
        return max_stated if max_stated > 0 else None
    
    def extract_technical_skills(self, resume_text: str) -> List[str]:
        """Extract technical skills with improved accuracy"""
        found_skills = set()
        text_lower = resume_text.lower()
        
        # Direct skill matching
        for skill in self.technical_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text_lower):
                found_skills.add(skill)
        
        # Context-based extraction
        skill_contexts = [
            r'(?:skills?|technologies?|tools?|frameworks?|languages?)[:\-]?\s*([^.]{1,200})',
            r'(?:proficient|experienced|expertise|familiar)\s+(?:with|in)\s+([^.]{1,100})',
            r'(?:knowledge|experience)\s+(?:of|in|with)\s+([^.]{1,100})'
        ]
        
        for pattern in skill_contexts:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                context = match.group(1)
                potential_skills = re.findall(r'\b[a-z]+(?:\.[a-z]+)*\b', context)
                for skill in potential_skills:
                    if skill in self.technical_skills:
                        found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def parse_resume_accurate(self, resume_text: str) -> Dict:
        """Main parsing function with improved accuracy"""
        # Extract experience section
        experience_section = self.extract_experience_section(resume_text)
        
        # Extract job entries
        job_entries = self.extract_job_entries(experience_section)
        
        # Calculate experience
        experience_data = self.calculate_total_experience(job_entries)
        
        # Extract stated experience
        stated_experience = self.extract_stated_experience(resume_text)
        
        # Extract technical skills
        technical_skills = self.extract_technical_skills(resume_text)
        
        # Final experience calculation (take the most reasonable value)
        final_experience = experience_data['total_years']
        if stated_experience and abs(stated_experience - final_experience) > 2:
            # If stated experience is significantly different, use the higher value
            final_experience = max(stated_experience, final_experience)
        
        return {
            'technical_skills': technical_skills,
            'experience': {
                'total_years': final_experience,
                'calculated_years': experience_data['total_years'],
                'stated_years': stated_experience,
                'total_months': experience_data['total_months'],
                'job_count': experience_data['job_count'],
                'job_details': experience_data['details'],
                'merged_periods': experience_data['merged_periods']
            },
            'parsing_quality': {
                'jobs_found': len(job_entries),
                'experience_section_found': bool(experience_section),
                'stated_experience_found': bool(stated_experience),
                'skills_found': len(technical_skills)
            }
        }

# # Usage function
# def parse_resume_enhanced(resume_text: str) -> Dict:
#     """Enhanced resume parser with accurate experience calculation"""
#     parser = AccurateResumeParser()
#     return parser.parse_resume_accurate(resume_text)

# # Example usage
# if __name__ == "__main__":
#     sample_resume = """
#     John Doe
#     Senior Software Engineer
    
#     WORK EXPERIENCE
    
#     Senior Software Engineer | ABC Tech | March 2020 - Present
#     • Developed web applications using React and Node.js
#     • Led team of 5 developers
    
#     Software Developer | XYZ Corp | June 2018 - February 2020
#     • Built APIs using Python and Django
#     • Worked with PostgreSQL and AWS
    
#     Junior Developer | StartupCo | January 2017 - May 2018
#     • Developed mobile apps using React Native
#     • Collaborated with cross-functional teams
    
#     TECHNICAL SKILLS
#     Programming: Python, JavaScript, React, Node.js, Django
#     Databases: PostgreSQL, MongoDB, Redis
#     Cloud: AWS, Docker, Kubernetes
#     """
    
#     result = parse_resume_enhanced(sample_resume)
#     print(f"Total Experience: {result['experience']['total_years']} years")
#     print(f"Jobs Found: {result['experience']['job_count']}")
#     print(f"Technical Skills: {result['technical_skills']}")
#     print(f"Job Details: {result['experience']['job_details']}")
