# Simple in-memory store
_interactions = []

async def store_interaction(jd_struct, res_struct, question, answer, eval_res, is_followup: bool = False):
    _interactions.append({
        'jd': jd_struct,
        'resume': res_struct,
        'question': question,
        'answer': answer,
        'evaluation': eval_res,
        'followup': is_followup
    })