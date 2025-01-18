import os
from vosk import Model, KaldiRecognizer
import wave
import pyaudio

class SpeechToTextService:
    def __init__(self, model_dir="vosk/models", model_name=None):
        """
        Inicializa el servicio de reconocimiento de voz.

        Args:
            model_dir (str): Ruta a la carpeta que contiene los modelos Vosk.
            model_name (str, opcional): Nombre del modelo a usar. Si no se especifica, se usará el primero encontrado.
        """
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"Model directory not found: {model_dir}")
        
        available_models = [d for d in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, d))]
        if not available_models:
            raise FileNotFoundError(f"No models found in: {model_dir}")
        
        if model_name:
            if model_name not in available_models:
                raise FileNotFoundError(f"Model '{model_name}' not found in: {model_dir}")
            selected_model_path = os.path.join(model_dir, model_name)
        else:
            selected_model_path = os.path.join(model_dir, available_models[0])
        
        print(f"Using Vosk model: {selected_model_path}")
        self.model = Model(selected_model_path)
        
        
    def listen_and_transcribe(self):
        """
        """
        recognizer = KaldiRecognizer(self.model, 16000)
        mic = pyaudio.PyAudio()
        
        stream = mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            frames_per_buffer=4096
        )
        stream.start_stream()
        
        print("Start listening...")
        transcript = ""
        try:
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    transcript += result
                    break
        except KeyboardInterrupt:
            print("Stopped listening")
        finally:
            stream.stop_stream()
            stream.close()
            mic.terminate()
            
        return transcript
    
    def process_audio(self, audio_file):
        """
        Convierte un archivo de audio a texto.

        Args:
            audio_file: Archivo de audio en formato WAV.

        Returns:
            str: Texto reconocido en el audio.
        """
        wf = wave.open(audio_file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            raise ValueError("Invalid audio format. Ensure mono WAV with 16-bit PCM.")
        
        rec = KaldiRecognizer(self.model, wf.getframerate())
        text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text += rec.Result()
        return text