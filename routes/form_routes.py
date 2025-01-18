from flask import Blueprint, request, jsonify
from models import get_form_data_collection
from models.form_data import FormDataModel

form_routes = Blueprint("form_routes", __name__)

@form_routes.before_app_first_request
def setup_model():
    """
    Configura el modelo de datos del formulario antes de procesar las solicitudes.
    """
    mongo = request.app.config["MONGO"]
    collection = get_form_data_collection(mongo)
    form_routes.form_data_model = FormDataModel(collection)

@form_routes.route("/submit-form", methods=["POST"])
def submit_form():
    """
    Ruta para guardar datos del formulario.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        form_id = form_routes.form_data_model.insert_form_data(data)
        return jsonify({"message": "Form data saved", "id": form_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@form_routes.route("/form-data", methods=["GET"])
def get_all_form_data():
    """
    Ruta para recuperar todos los datos del formulario.
    """
    try:
        data = form_routes.form_data_model.get_all_form_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500