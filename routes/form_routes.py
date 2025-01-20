from flask import Blueprint, request, jsonify
from services import get_speech_to_text_service, get_translation_service

form_routes = Blueprint("form_routes", __name__)


@form_routes.route("/speech-to-text/live", methods=["GET"])
def speech_to_text_live():
    """
    Escucha desde el micrófono y convierte el audio a texto.
    """
    try:
        speech_service = get_speech_to_text_service()
        text = speech_service.listen_and_transcribe()
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@form_routes.route("/translate", methods=["POST"])
def translate():
    """
    Ruta para traducir texto entre idiomas.
    """
    data = request.json
    if not data or not all(key in data for key in ("text", "src_lang", "target_lang")):
        return jsonify({"error": "Invalid input. Provide 'text', 'src_lang', and 'target_lang'."}), 400

    try:
        translation_service = get_translation_service()
        translated_text = translation_service.translate_text(
            text=data["text"],
            src_lang=data["src_lang"],
            target_lang=data["target_lang"],
        )
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@form_routes.route("/speech-to-text-translate", methods=["GET"])
def speech_to_text_and_translate():
    """
    Escucha desde el micrófono, convierte el audio a texto y lo traduce al español.
    """
    try:

        speech_service = get_speech_to_text_service()
        translation_service = get_translation_service()


        text = speech_service.listen_and_transcribe()

        # detect language
        detected_language = translation_service.detect_language(text)
        

        src_lang = "en" if text.isascii() else "fr"


        translated_text = translation_service.translate_text(
            text=text,
            src_lang=detected_language,
            target_lang="es"
        )

        return jsonify({
            "original_text": text,
            "source_language": src_lang,
            "translated_text": translated_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@form_routes.route("/speech-to-text-translate-live", methods=["GET"])
def speech_to_text_and_translate_live():
    """
    Escucha desde el micrófono, detecta el idioma en tiempo real, transcribe y traduce al español.
    """
    try:
        speech_service = get_speech_to_text_service()
        translation_service = get_translation_service()

        text, detected_language = speech_service.listen_and_transcribe_with_language()

        if not detected_language:
            return jsonify({"error": "Unable to detect language."}), 400

        translated_text = translation_service.translate_text(
            text=text,
            src_lang=detected_language,
            target_lang="es"
        )

        return jsonify({
            "original_text": text,
            "source_language": detected_language,
            "translated_text": translated_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500