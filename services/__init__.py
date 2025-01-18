from .vosk_service import SpeechToTextService

# Ruta al modelo Vosk
VOSK_MODEL_PATH = "models/vosk"

# Crear una instancia global del servicio de Speech-to-Text
speech_to_text_service = SpeechToTextService(model_path=VOSK_MODEL_PATH)

def get_speech_to_text_service():
    """
    Devuelve una instancia del servicio de reconocimiento de voz.
    """
    return speech_to_text_service