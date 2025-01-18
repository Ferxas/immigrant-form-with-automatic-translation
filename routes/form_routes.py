from flask import Blueprint, request, jsonify
from services import get_speech_to_text_service, get_translation_service

form_routes = Blueprint("form_routes", __name__)


@form_routes.route("/speech-to-text/live", methods=["GET"])
def speech_to_text():
    """
    Escucha el micrófono y lo convierte a texto
    """
    file = request.files.get("audio")
    # Pasar el modelo como parámetro opcional
    model_name = request.args.get("model")

    if not file:
        return jsonify({"error": "No audio file provided"}), 400

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
