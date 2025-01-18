from flask import Blueprint, request, jsonify
from services.translation_service import TranslationService

form_routes = Blueprint("form_routes", __name__)

# Inicializar el servicio de traducción
translator = TranslationService()

@form_routes.route("/translate", methods=["POST"])
def translate():
    """
    Ruta para traducir texto entre idiomas.
    """
    data = request.json
    if not data or not all(key in data for key in ("text", "src_lang", "target_lang")):
        return jsonify({"error": "Invalid input. Provide 'text', 'src_lang', and 'target_lang'."}), 400

    try:
        translated_text = translator.translate_text(
            text=data["text"],
            src_lang=data["src_lang"],
            target_lang=data["target_lang"],
        )
        return jsonify({"translated_text": translated_text})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500