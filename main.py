from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from supabase_client import store_message, fetch_memory
import os

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now, restrict if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Health route (GET /)
@app.get("/")
async def root():
    return {"status": "MAYO backend is alive"}

# Request model
class UserMessage(BaseModel):
    user_id: str
    message: str

# Chat route (POST /chat)
@app.post("/chat")
async def chat_with_gpt(data: UserMessage):
    memory_context = fetch_memory(data.user_id)

    # Prompt with memory
    prompt = f"""
You are MAYOAIAGENT — a master-level, spiritual, creative AI agent for power and transformation.
Use memory, talk like Cheef, and answer with clarity and depth.

Memory:
{memory_context}

User: {data.message}
AI:"""

    # GPT-4 call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are MAYOAIAGENT. Respond with spiritual, street-smart, creative power."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()

    # Store in Supabase
    store_message(data.user_id, data.message, reply)

    return {"response": reply}
