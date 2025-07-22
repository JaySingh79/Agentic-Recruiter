from utils.vector_db import VectorDB
import asyncio


vector_db = VectorDB()

async def match_skills(jd_struct: list, resume_struct: list) -> list:
    matches = {}
    for skill in jd_struct:
        found = await vector_db.similarity_search(skill, resume_struct, top_k=1)
        matches[skill] = found[0] if found else None
    return [result for result in matches.values() if result is not None]


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
#     response = await match_skills(jd_skills_testing, resume_skills_testing)
#     print(response)
    
    
# asyncio.run(main())