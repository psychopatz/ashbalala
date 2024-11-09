from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from enum import Enum
import os


class AzureVoice:
    voices = {
        "EN_US_JENNY": "en-US-JennyNeural",
        "EN_US_GUY": "en-US-GuyNeural",
        "EN_GB_RYAN": "en-GB-RyanNeural",
    }


class AzureTTSProvider:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_SERVICE_REGION")

    def synthesize(self, text, audio_path, voice=None):
        if voice is None:
            voice = "en-US-JennyNeural"  # Default voice
        speech_config = SpeechConfig(subscription=self.speech_key, region=self.region)
        if voice:
            speech_config.speech_synthesis_voice_name = voice
        audio_config = AudioOutputConfig(filename=audio_path)
        synthesizer = SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        result = synthesizer.speak_text(text)
        return result.reason == ResultReason.SynthesizingAudioCompleted
