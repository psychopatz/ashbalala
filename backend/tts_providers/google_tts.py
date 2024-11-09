from google.cloud import texttospeech
from enum import Enum
import os


class GoogleVoice:
    voices = {
        "EN_US_STANDARD_B": "en-US-Standard-B",
        "EN_US_STANDARD_C": "en-US-Standard-C",
        "EN_GB_WAVENET_A": "en-GB-Wavenet-A",
    }


class GoogleTTSProvider:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, text, audio_path, voice=None):
        if voice is None:
            voice = "en-US-JennyNeural"  # Default voice
        input_text = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice if voice else "en-US-Standard-B",  # Default voice
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = self.client.synthesize_speech(
            input=input_text, voice=voice_params, audio_config=audio_config
        )
        with open(audio_path, "wb") as out:
            out.write(response.audio_content)
        return True
