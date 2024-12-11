from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.voices import tts, get_voices
from app.services.azure_services import token_manager, voice_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tts.router)
app.include_router(get_voices.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
