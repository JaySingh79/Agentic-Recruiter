from utils.resume_parser import AccurateResumeParser
from utils.jd_parser import ComprehensiveSkillExtractor

extractor_here = ComprehensiveSkillExtractor()
crazy_resume_parser = AccurateResumeParser()

class parse_inputs:
    @staticmethod
    async def parse_jd(jd_text: str):
        return extractor_here.extract_all_skills(jd_text)

    @staticmethod
    async def parse_resume_text(resume_text: str):
        result = crazy_resume_parser.parse_resume_accurate(resume_text)
        return [result['technical_skills'], result['experience']['total_years']]