import os
from vosk import Model, KaldiRecognizer
import wave

class SpeechToTextService:
    def __init__(self, model_path="vosk/models"):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model not found.")
        self.model = Model(model_path)
    
    def process_audio(self, audio_file):
        wf = wave.open(audio_file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            raise ValueError("Invalid audio format")
        
        rec = KaldiRecognizer(self.model, wf.getframerate())
        text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text += rec.Result()
        return text