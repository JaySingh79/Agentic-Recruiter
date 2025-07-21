import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def call_llm(prompt: str) -> str:
    response = await async_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role":"user", "content":prompt}]
    )
    
    return response.choices[0].message.content

async def main():
    print("Answer is coming..\n")
    result = await call_llm("Give me 5 best pdf parsing methods. Keep it short. Write in bullet points")
    print(result)


asyncio.run(main())