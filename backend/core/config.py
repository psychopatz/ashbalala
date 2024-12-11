import os
from datetime import timedelta

# ---------------------------------------------------------
# Azure Configuration 
# ---------------------------------------------------------

# Azure configuration variables
AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
AZURE_REGION = os.getenv("AZURE_REGION", "eastus")

AZURE_TOKEN_URL = f"https://{AZURE_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
AZURE_TTS_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
AZURE_VOICES_URL = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/voices/list"

# Token expiry and voices update intervals
TOKEN_EXPIRY_MINUTES = 9
VOICES_UPDATE_INTERVAL = timedelta(hours=24)

# Default TTS settings
DEFAULT_VOICE = "en-US-JennyNeural"
DEFAULT_STYLE = "neutral"
DEFAULT_RATE = "+0%"
DEFAULT_PITCH = "+0Hz"

# Audio file storage directory
AUDIO_FILES_DIR = "audio_files"
os.makedirs(AUDIO_FILES_DIR, exist_ok=True)

# ---------------------------------------------------------
# OpenDrive Configuration 
# ---------------------------------------------------------
OPENDRIVE_BASE_URL = os.getenv("OPENDRIVE_BASE_URL", "https://dev.opendrive.com/api/v1")
OPENDRIVE_USERNAME = os.getenv("OPENDRIVE_USERNAME")
OPENDRIVE_PASSWORD = os.getenv("OPENDRIVE_PASSWORD")
