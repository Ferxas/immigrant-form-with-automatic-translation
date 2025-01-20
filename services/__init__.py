from .vosk_service import SpeechToTextService
from .translation_service import TranslationService

# Configuración inicial
DEFAULT_VOSK_MODEL_DIR = "vosk/models"
DEFAULT_VOSK_MODEL_NAME = None  # default model, for example -> "model1"

# Instancias globales si necesitas reutilizar servicios con configuraciones comunes
translation_service = TranslationService()

def get_translation_service():
    """
    Devuelve una instancia del servicio de traducción.
    """
    return translation_service

def get_speech_to_text_service(model_name=None):
    """
    Devuelve una instancia del servicio de reconocimiento de voz.
    
    Args:
        model_name (str, opcional): Nombre del modelo Vosk. Si no se especifica, usa el modelo por defecto.

    Returns:
        SpeechToTextService: Instancia del servicio.
    """
    return SpeechToTextService(model_path=DEFAULT_VOSK_MODEL_DIR, model_name=model_name)
