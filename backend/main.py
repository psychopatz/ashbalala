from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import tts, voices

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tts.router, prefix="/tts", tags=["Text-to-Speech"])
app.include_router(voices.router, prefix="/voices", tags=["Voices"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
