from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import CORS_ORIGINS, engine, SessionLocal
from models.audiobook.audiobook_model import Base
from routers.tts import tts as tts_router
from routers.tts import voices as voices_router
from routers.opendrive import auth as auth_router
from routers.opendrive import folder as folder_router
from routers.opendrive import file as file_router
from routers.audiobook import audiobook as audiobook_router
from routers.audiobook import chapter as chapter_router
from routers.audiobook import genre as genre_router
from routers.audiobook import category as category_router
from routers.audiobook import tag as audiobook_tag_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tts_router.router, prefix="/tts", tags=["Text-to-Speech"])
app.include_router(voices_router.router, prefix="/voices", tags=["Voices"])
app.include_router(auth_router.router, prefix="/opendrive", tags=["OpenDrive Auth"])
app.include_router(folder_router.router, prefix="/opendrive", tags=["OpenDrive Folder"])
app.include_router(file_router.router, prefix="/opendrive", tags=["OpenDrive File"])
app.include_router(audiobook_router.router, prefix="/audiobooks", tags=["Audiobooks"])
app.include_router(chapter_router.router, prefix="/chapters", tags=["Chapters"])
app.include_router(genre_router.router, prefix="/genres", tags=["Genres"])
app.include_router(category_router.router, prefix="/categories", tags=["Categories"])
app.include_router(
    audiobook_tag_router.router, prefix="/audiobook_tags", tags=["Audiobook Tags"]
)


@app.get("/")
async def root():
    return {"message": "Welcome to Ashbalala Backend"}


# Initialize database
Base.metadata.create_all(bind=engine)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
