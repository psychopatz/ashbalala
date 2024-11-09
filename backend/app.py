# app.py
from fastapi import FastAPI
from routes import upload, convert, download
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Directory to store uploaded eBook files and audio files
UPLOAD_DIR = "uploads"
AUDIO_DIR = "audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

app.include_router(upload.router)
app.include_router(convert.router)
app.include_router(download.router)
