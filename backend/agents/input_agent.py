from utils.gemini_for_parsing import resume_parser
from utils.gemini_for_parsing import jd_parser

# extractor_here = ComprehensiveSkillExtractor()
# crazy_resume_parser = AccurateResumeParser()

class parse_inputs:
    @staticmethod
    async def parse_jd(jd_text: str):
        return jd_parser(jd_text)

    @staticmethod
    async def parse_resume_text(resume_text: str):
        result = resume_parser(resume_text)
        # return [result['technical_skills'], result['experience']['total_years']]
        return result