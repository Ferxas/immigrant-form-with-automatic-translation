import os
from vosk import Model, KaldiRecognizer
import wave
import pyaudio
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class SpeechToTextService:
    def __init__(self, model_path="vosk/models", model_name=None):
        """
        Inicializa el servicio de reconocimiento de voz.

        Args:
            model_path (str): Ruta a la carpeta que contiene los modelos Vosk.
            model_name (str, opcional): Nombre del modelo a usar.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model directory not found: {model_path}")
        
        # Buscar y seleccionar el modelo adecuado
        available_models = [d for d in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, d))]
        if not available_models:
            raise FileNotFoundError(f"No models found in: {model_path}")
        
        if model_name:
            if model_name not in available_models:
                raise FileNotFoundError(f"Model '{model_name}' not found in: {model_path}")
            selected_model_path = os.path.join(model_path, model_name)
        else:
            selected_model_path = os.path.join(model_path, available_models[0])
        
        print(f"Using Vosk model: {selected_model_path}")
        self.model = Model(selected_model_path)

    def listen_and_transcribe(self):
        """
        Escucha desde el micrófono y transcribe el audio en tiempo real.

        Returns:
            str: Texto reconocido.
        """
        recognizer = KaldiRecognizer(self.model, 16000)
        mic = pyaudio.PyAudio()

        stream = mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )
        stream.start_stream()

        print("Listening...")
        transcript = ""
        try:
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    transcript += result
                    break  # Puedes detenerte en el primer reconocimiento completo
        except KeyboardInterrupt:
            print("Stopped listening.")
        finally:
            stream.stop_stream()
            stream.close()
            mic.terminate()

        return transcript


    def listen_and_transcribe_with_language(self):
        """
        Escucha desde el micrófono, transcribe el audio y detecta el idioma en tiempo real.

        Returns:
            tuple: Texto transcrito y el idioma detectado (código ISO, ej. 'en', 'fr').
        """
        recognizer = KaldiRecognizer(self.model, 16000)
        mic = pyaudio.PyAudio()
        
        stream = mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )
        stream.start_stream()

        print("Listening...")
        transcript = ""
        detected_language = None
        try:
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    partial_text = eval(result).get("text", "")  # Obtener texto parcial
                    
                    if partial_text.strip():
                        # Detectar idioma sobre el texto parcial
                        detected_language = detect(partial_text)
                        transcript += partial_text + " "
                        print(f"Detected language: {detected_language}")
                        break  # Finalizar en el primer resultado completo
        except KeyboardInterrupt:
            print("Stopped listening.")
        finally:
            stream.stop_stream()
            stream.close()
            mic.terminate()
        
        return transcript.strip(), detected_language

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
            raise ValueError(
                "Invalid audio format. Ensure mono WAV with 16-bit PCM.")

        rec = KaldiRecognizer(self.model, wf.getframerate())
        text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text += rec.Result()
        return text
