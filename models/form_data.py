from bson import ObjectId

class FormDataModel:
    def __init__(self, collection):
        self.collection = collection

    def insert_form_data(self, form_data):
        """
        Inserta datos del formulario en la base de datos.

        Args:
            form_data (dict): Los datos del formulario a insertar.

        Returns:
            str: El ID del documento insertado.
        """
        result = self.collection.insert_one(form_data)
        return str(result.inserted_id)

    def get_all_form_data(self):
        """
        Recupera todos los datos del formulario.

        Returns:
            list: Lista de documentos del formulario.
        """
        return [
            {**doc, "_id": str(doc["_id"])}
            for doc in self.collection.find()
        ]

    def get_form_data_by_id(self, form_id):
        """
        Recupera un documento específico por su ID.

        Args:
            form_id (str): El ID del documento.

        Returns:
            dict: Los datos del formulario o None si no se encuentra.
        """
        document = self.collection.find_one({"_id": ObjectId(form_id)})
        if document:
            document["_id"] = str(document["_id"])
        return document