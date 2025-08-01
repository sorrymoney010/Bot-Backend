from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_memory(user_id):
    response = supabase.table("chat_memory") \
        .select("user_message, ai_response") \
        .eq("user_id", user_id) \
        .order("timestamp", desc=False) \
        .limit(10) \
        .execute()
    messages = response.data
    return "\n".join([f"User: {m['user_message']}\nAI: {m['ai_response']}" for m in messages]) if messages else ""

def store_message(user_id, user_message, ai_response):
    supabase.table("chat_memory").insert({
        "user_id": user_id,
        "user_message": user_message,
        "ai_response": ai_response
    }).execute()
