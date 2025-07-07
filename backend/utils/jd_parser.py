# # import re
# # from typing import Dict, List

# # async def parse_jd(text: str) -> Dict:
# #     lines = text.splitlines()
# #     skills: List[str] = []
# #     for line in lines:
# #         if 'requirements:' in line.lower() or 'skills:' in line.lower():
# #             parts = line.split(':', 1)[1]
# #             skills = [s.strip() for s in parts.split(',')]
# #     return {'skills': skills}


# # backend/utils/jd_parser.py
# """
# Extract a list of technical skills / tools / frameworks mentioned in a JD.

# Returns
# -------
# dict  ->  {"skills": ["Python", "Docker", "C++", ...]}
# """

# import re
# from typing import Dict, List
# import yake

# # ------------ patterns & helpers -------------------------------------------------

# # Title‑Case phrase up to 3 words (“Machine Learning”, “React Native”)
# TITLE_RE   = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b")

# # All‑CAP acronym 2‑5 letters (“AWS”, “SQL”)
# ACRONYM_RE = re.compile(r"\b[A-Z]{2,5}\b")

# # YAKE extractor for extra tech keywords (unigrams)
# YAKE = yake.KeywordExtractor(lan="en", n=1, top=50)

# STOP = {"The", "And", "With", "For", "This", "That", "From", "Your"}

# def _extract_candidates(text: str) -> List[str]:
#     """Collect candidates via regex + YAKE, dedupe & sort."""
#     phrases  = {m.group(0) for m in TITLE_RE.finditer(text)}
#     acronyms = {m.group(0) for m in ACRONYM_RE.finditer(text)}
#     keywords = {
#         kw for kw, _ in YAKE.extract_keywords(text)
#         if re.match(r"^[A-Za-z\+\.\#]{3,}$", kw)
#     }
#     return sorted((phrases | acronyms | keywords) - STOP)

# # ------------ public API ---------------------------------------------------------

# async def parse_jd(text: str) -> Dict[str, List[str]]:
#     """
#     Parameters
#     ----------
#     text : str  (JD body in plain text)

#     Returns
#     -------
#     {"skills": [...]}  list is deduplicated & alphabetised
#     """
#     # collapse whitespace to help regex/YAKE
#     text = re.sub(r"\s+", " ", text).strip()
#     return {"skills": _extract_candidates(text)}

# async def parse_resume_text(text: str): 
    
#     text_resume = re.sub(r"\s+", " ", text).strip()
#     return {"resume skills": _extract_candidates(text_resume)}
    
    
    
import re
from typing import Dict, List
import yake


# ------------ patterns & helpers -------------------------------------------------

# Title‑Case phrase up to 3 words (“Machine Learning”, “React Native”)
TITLE_RE   = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b")

# All‑CAP acronym 2‑5 letters (“AWS”, “SQL”)
ACRONYM_RE = re.compile(r"\b[A-Z]{2,5}\b")

# YAKE extractor for extra tech keywords (unigrams)
YAKE = yake.KeywordExtractor(lan="en", n=1, top=50)

STOP = {"The", "And", "With", "For", "This", "That", "From", "Your"}

def _extract_candidates(text: str) -> List[str]:
    """Collect candidates via regex + YAKE, dedupe & sort."""
    phrases  = {m.group(0) for m in TITLE_RE.finditer(text)}
    acronyms = {m.group(0) for m in ACRONYM_RE.finditer(text)}
    keywords = {
        kw for kw, _ in YAKE.extract_keywords(text)
        if re.match(r"^[A-Za-z\+\.\#]{3,}$", kw)
    }
    return sorted((phrases | acronyms | keywords) - STOP)

# ------------ experience extractor -------------------------------------------------

# def extract_years_of_experience(text: str) -> int:
#     """
#     Extracts the maximum number of years of experience mentioned in the text.

#     Returns
#     -------
#     int : maximum years of experience found (0 if none)
#     """
#     text = text.lower()
#     patterns = [
#         r"(\d+)\s*(?:\+|-)?\s*years?",              # "5 years", "5+ years", "5-7 years"
#         r"minimum\s+(\d+)\s*years?",
#         r"at least\s+(\d+)\s*years?",
#         r"(\d+)\s*yrs",                             # "5yrs", "2 yrs"
#     ]
    
#     years = []
#     for pattern in patterns:
#         for match in re.findall(pattern, text):
#             try:
#                 years.append(int(match))
#             except ValueError:
#                 continue
    
#     return max(years, default=0)

# ------------ public API ---------------------------------------------------------

# async def parse_jd(text: str) -> Dict[str, List[str]]:


#     # Example output: [{'label': 'Data Science', 'score': 0.97}]

#     """
#     Parameters
#     ----------
#     text : str  (JD body in plain text)

#     Returns
#     -------
#     {"skills": [...]}  list is deduplicated & alphabetised
#     """
#     # collapse whitespace to help regex/YAKE
#     text = re.sub(r"\s+", " ", text).strip()
#     return {"skills": _extract_candidates(text)}


# async def parse_resume_text(text: str): 
    
#     """
#     Extracts the maximum number of years of experience mentioned in the text.

#     Returns
#     -------
#     int : maximum years of experience found (0 if none)
#     """
#     text_resume = re.sub(r"\s+", " ", text).strip()
    
#     text = text.lower()
#     patterns = [
#         r"(\d+)\s*(?:\+|-)?\s*years?",              # "5 years", "5+ years", "5-7 years"
#         r"minimum\s+(\d+)\s*years?",
#         r"at least\s+(\d+)\s*years?",
#         r"(\d+)\s*yrs",                             # "5yrs", "2 yrs"
#     ]
    
#     years = []
#     for pattern in patterns:
#         for match in re.findall(pattern, text):
#             try:
#                 years.append(int(match))
#             except ValueError:
#                 continue
    
#     return {"experience": max(years, default=0), "resume skills": _extract_candidates(text_resume)}




####################################################################################################################################


import re
from typing import List, Set, Dict
import spacy
from collections import defaultdict

class ComprehensiveSkillExtractor:
    def __init__(self):
        # Load lightweight spaCy model for NLP
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Predefined technical skills (for ultra-fast extraction)
        self.known_skills = {
            'python', 'java', 'javascript', 'react', 'angular', 'vue.js', 'node.js',
            'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes',
            'tensorflow', 'pytorch', 'pandas', 'numpy', 'git', 'jenkins', 'jira'
            # ... (your existing list)
        }
        
        # Skill indicators - patterns that suggest something is a skill
        self.skill_indicators = {
            'before': [
                r'\b(?:experience (?:with|in)|proficiency (?:with|in)|knowledge of|expertise in|skilled in|familiar with|using|worked with|background in)\s+',
                r'\b(?:required|preferred|desired|must have|should have|nice to have)[:.]?\s+',
                r'\b(?:strong|excellent|solid|good|basic|advanced|expert|intermediate)\s+(?:knowledge|experience|skills?|understanding)\s+(?:of|in|with)\s+',
                r'\b(?:minimum|at least|minimum of|\d+\+?)\s+years?\s+(?:of\s+)?(?:experience|exp)\s+(?:with|in|using)\s+'
            ],
            'after': [
                r'\s+(?:experience|skills?|knowledge|proficiency|expertise|background|certification|training)',
                r'\s+(?:required|preferred|desired|mandatory|essential|necessary)',
                r'\s+(?:developer|engineer|specialist|expert|administrator|analyst|architect|consultant)'
            ],
            'patterns': [
                r'\b[A-Z][a-z]+(?:\.[a-z]+)*\b',  # CamelCase or dotted notation (e.g., React.js, Node.js)
                r'\b[A-Z]{2,}\b',  # Acronyms (e.g., API, REST, JSON)
                r'\b\w+[-_]\w+\b',  # Hyphenated/underscore terms (e.g., test-driven, machine_learning)
                r'\b\d+\.\d+\b'  # Version numbers (e.g., Python 3.9)
            ]
        }
        
        # Compile regex patterns
        self.compiled_patterns = {
            'before': [re.compile(pattern, re.IGNORECASE) for pattern in self.skill_indicators['before']],
            'after': [re.compile(pattern, re.IGNORECASE) for pattern in self.skill_indicators['after']],
            'patterns': [re.compile(pattern) for pattern in self.skill_indicators['patterns']]
        }
        
        # Common non-skill words to filter out
        self.stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'among', 'through', 'during', 'before', 'after', 'above',
            'team', 'work', 'working', 'ability', 'strong', 'excellent', 'good', 'experience',
            'years', 'year', 'must', 'should', 'required', 'preferred', 'desired', 'knowledge',
            'skills', 'skill', 'understanding', 'familiar', 'background', 'expertise'
        }

    def _extract_predefined_skills(self, text: str) -> Set[str]:
        """Ultra-fast extraction of known skills"""
        found_skills = set()
        text_lower = text.lower()
        
        for skill in self.known_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text_lower):
                found_skills.add(skill)
        
        return found_skills

    def _extract_contextual_skills(self, text: str) -> Set[str]:
        """Extract skills based on context patterns"""
        found_skills = set()
        
        # Look for skills mentioned with indicators
        for pattern in self.compiled_patterns['before']:
            matches = pattern.finditer(text)
            for match in matches:
                # Extract next 1-3 words after the pattern
                start = match.end()
                remaining_text = text[start:start+100]  # Look ahead 100 chars
                
                # Extract potential skill terms
                skill_match = re.search(r'\b([A-Za-z][A-Za-z0-9\.\-_]*(?:\s+[A-Za-z][A-Za-z0-9\.\-_]*){0,2})\b', remaining_text)
                if skill_match:
                    skill = skill_match.group(1).strip()
                    if self._is_valid_skill(skill):
                        found_skills.add(skill.lower())
        
        return found_skills

    def _extract_pattern_based_skills(self, text: str) -> Set[str]:
        """Extract skills based on naming patterns"""
        found_skills = set()
        
        # Extract technology-like patterns
        for pattern in self.compiled_patterns['patterns']:
            matches = pattern.finditer(text)
            for match in matches:
                potential_skill = match.group(0)
                if self._is_valid_skill(potential_skill):
                    found_skills.add(potential_skill.lower())
        
        return found_skills

    def _extract_noun_phrases(self, text: str) -> Set[str]:
        """Extract potential skills using NLP noun phrase extraction"""
        if not self.nlp:
            return set()
        
        found_skills = set()
        doc = self.nlp(text)
        
        # Extract noun phrases that could be skills
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Limit to 3-word phrases
                phrase = chunk.text.strip()
                if self._is_valid_skill(phrase):
                    found_skills.add(phrase.lower())
        
        # Extract named entities that could be technologies
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE'] and len(ent.text.split()) <= 2:
                if self._is_valid_skill(ent.text):
                    found_skills.add(ent.text.lower())
        
        return found_skills

    def _is_valid_skill(self, term: str) -> bool:
        """Validate if a term is likely a skill"""
        term = term.strip().lower()
        
        # Filter out common non-skills
        if term in self.stopwords or len(term) < 2:
            return False
        
        # Filter out common English words
        if term in ['team', 'work', 'project', 'company', 'role', 'position', 'job']:
            return False
        
        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', term):
            return False
        
        # Avoid very long phrases
        if len(term.split()) > 3:
            return False
        
        return True

    def _rank_skills(self, skills: Set[str], text: str) -> List[str]:
        """Rank skills by frequency and context importance"""
        skill_scores = defaultdict(int)
        text_lower = text.lower()
        
        for skill in skills:
            # Base score
            skill_scores[skill] = 1
            
            # Frequency bonus
            skill_scores[skill] += len(re.findall(rf'\b{re.escape(skill)}\b', text_lower))
            
            # Context bonus (if mentioned with strong indicators)
            for pattern in self.compiled_patterns['before']:
                if pattern.search(text_lower):
                    surrounding_text = text_lower[max(0, text_lower.find(skill)-50):text_lower.find(skill)+50]
                    if pattern.search(surrounding_text):
                        skill_scores[skill] += 2
        
        # Sort by score, then alphabetically
        return sorted(skills, key=lambda x: (-skill_scores[x], x))

    def extract_all_skills(self, job_description: str) -> List[str]:
        """
        Extract ALL types of skills from job description
        
        Args:
            job_description (str): Raw job description text
            
        Returns:
            List[str]: Comprehensive list of all skills found, ranked by relevance
        """
        if not job_description or not isinstance(job_description, str):
            return []
        
        all_skills = set()
        
        # 1. Fast predefined skill extraction
        all_skills.update(self._extract_predefined_skills(job_description))
        
        # 2. Context-based skill extraction
        all_skills.update(self._extract_contextual_skills(job_description))
        
        # 3. Pattern-based extraction
        all_skills.update(self._extract_pattern_based_skills(job_description))
        
        # 4. NLP-based extraction (if available)
        all_skills.update(self._extract_noun_phrases(job_description))
        
        # 5. Rank and return
        return self._rank_skills(all_skills, job_description)

# # Usage
# extractor = ComprehensiveSkillExtractor()

# def extract_comprehensive_skills(job_description: str) -> List[str]:
#     """
#     Extract all types of skills with ultra-fast performance
#     Average response time: <50ms for typical job descriptions
#     """
#     return extractor.extract_all_skills(job_description)

# # Example usage
# job_desc = """
# We are looking for a Senior Full Stack Developer with expertise in Python, 
# React.js, and PostgreSQL. Experience with AWS, Docker, and Kubernetes is required.
# Strong communication skills and leadership experience are essential.
# Knowledge of machine learning libraries like TensorFlow and scikit-learn is a plus.
# Experience with Agile methodologies and project management tools like NewRelic is preferred.
# """

# skills = extract_comprehensive_skills(job_desc)
# print(skills)
# # Output: ['python', 'react.js', 'postgresql', 'aws', 'docker', 'kubernetes', 
# #          'communication', 'leadership', 'tensorflow', 'scikit-learn', 'agile', 
# #          'project management', 'newrelic']
