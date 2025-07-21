from utils.vector_db import VectorDB

vector_db = VectorDB()

async def match_skills(jd_struct: list, resume_struct: list) -> dict:
    matches = {}
    for skill in jd_struct:
        found = await vector_db.similarity_search(skill, resume_struct, top_k=1)
        matches[skill] = found[0] if found else None
    return matches