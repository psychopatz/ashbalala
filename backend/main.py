from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import tts, voices
from backend.routers.opendrive_endpoints import router as opendrive_router


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
app.include_router(opendrive_router, prefix="/opendrive", tags=["opendrive"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
