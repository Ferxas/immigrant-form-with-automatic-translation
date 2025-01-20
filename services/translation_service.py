from googletrans import Translator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        
    def detect_language(self, text):
        try:
            return detect(text)
        except Exception as e:
            raise RuntimeError(f"Error detecting language {e}")

    def translate_text(self, text, src_lang, target_lang):
        """
        Traduce un texto de un idioma a otro.

        Args:
            text (str): Texto a traducir.
            src_lang (str): Código del idioma fuente (ej., 'en' para inglés).
            target_lang (str): Código del idioma destino (ej., 'fr' para francés).

        Returns:
            str: Texto traducido.
        """
        try:
            translation = self.translator.translate(text, src=src_lang, dest=target_lang)
            return translation.text
        except Exception as e:
            raise RuntimeError(f"Error during translation: {e}")