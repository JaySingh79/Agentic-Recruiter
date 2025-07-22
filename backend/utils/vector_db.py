from sentence_transformers import SentenceTransformer, util
import asyncio

model = SentenceTransformer('all-MiniLM-L6-v2')

class VectorDB:
    async def similarity_search(self, query: str, corpus: list, top_k: int = 1):
        q_emb = model.encode(query, convert_to_tensor=True)
        c_emb = model.encode(corpus, convert_to_tensor=True)
        hits = util.semantic_search(q_emb, c_emb, top_k=top_k)[0]
        return [corpus[h['corpus_id']] for h in hits if h['score']>0.7]
        # return hits
    
    
    
# vector_db = VectorDB()

# async def match_skills(jd_struct: list, resume_struct: list):
#     matches = {}
#     for skill in jd_struct:
#         found = await vector_db.similarity_search(skill, resume_struct, top_k=1)
#         matches[skill] = found[0] if found else None
#     return matches


# async def matching_skill():
    
#     response = await vector_db.similarity_search(resume_skills_testing[0], jd_skills_testing)
#     print(response)
    
    
# jd_skills_testing = ['python', 'langchain', 'haystack', 
#                      'pydantic ai', 'openai', 'anthropic',
#                      'mcp', 'aws', 'gcp', 'cors', 'anthropic',
#                      'hugging face',
#                     'flan t5 xl', 'llms', 'render', 'streamlit', 'pca',
#                     'random forest', 'gradient boosting', 'pytorch',
#                     'aws', 'ec2', 'sagemaker','docker', 'k8s']


# resume_skills_testing = ['python', 'probability and statistics',
#                          'machine learning', 'lda', 'langchain',
#                          'cot', 'zsl', 'rag', 'gpt-4o', 'slms', 't5',
#                          'fp16', 'a100', 'lora', 'bleu', 'rouge-l',
#                          'kubeflow', 'mlflow', 'triton', 'groq api',
#                          'restful', 'cors', 'anthropic', 'hugging face',
#                          'flan t5 xl', 'llms', 'render', 'streamlit', 'pca',
#                          'random forest', 'gradient boosting', 'pytorch',
#                          'aws', 'ec2', 'sagemaker', 'snowflake', 'flask',
#                          'fastapi', 'django', 'docker', 'sql', 'react',
#                          'kubernetes', 'git', 'github', 'plotly', 'gpt',
#                          'bert', 'tensorflow', 'scikit-learn', 'transformers', 
#                          'cnn', 'nlp', 'nlu', 'gans', 'federated learning',
#                          'text generation', 'tf-idf', 'recommender systems',
#                          'mlops', 'transfer learning', 'xgboost', 'lightgbm',
#                          'catboost', 'gridsearchcv']



# async def main():
#     response = await matching_skill()
#     print(response)
    
    
# asyncio.run(matching_skill())