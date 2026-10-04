from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from routers import matches

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Deploy ke baad apna Next.js Vercel URL yahan daal dena security ke liye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app.state.supabase = supabase
app.include_router(matches.router)

@app.get("/")
def home():
    return {"message": "Free Fire Tournament API is Live!"}