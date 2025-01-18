def get_form_data_collection(mongo):
    """
    Devuelve la colección de datos del formulario desde MongoDB.

    Args:
        mongo: Instancia de PyMongo inicializada en Flask.

    Returns:
        Collection: Una referencia a la colección `form_data`.
    """
    return mongo.db.form_data