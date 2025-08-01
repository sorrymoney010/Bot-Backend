from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from supabase_client import store_message, fetch_memory
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_with_gpt(data: UserMessage):
    memory_context = fetch_memory(data.user_id)
    prompt = f"""
You are MAYOAIAGENT — a master-level, spiritual, creative AI agent for power and transformation.
Use memory, talk like Cheef, and answer with clarity and depth.

Memory:
{memory_context}

User: {data.message}
AI:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are MAYOAIAGENT. Respond with spiritual, street-smart, creative power."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()
    store_message(data.user_id, data.message, reply)
    return {"response": reply}
