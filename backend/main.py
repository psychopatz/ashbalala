from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import tts, voices
from backend.routers.opendrive import auth as auth_router
from backend.routers.opendrive import folder as folder_router
from backend.routers.opendrive import file as file_router

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
app.include_router(auth_router.router, prefix="/opendrive", tags=["OpenDrive Auth"])
app.include_router(folder_router.router, prefix="/opendrive", tags=["OpenDrive Folder"])
app.include_router(file_router.router, prefix="/opendrive", tags=["OpenDrive File"])

@app.get("/")
async def root():
    return {"message": "OpenDrive API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)