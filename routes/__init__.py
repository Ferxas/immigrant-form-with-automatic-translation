from .form_routes import form_routes

def init_routes(app, mongo):
    app.config["MONGO"] = mongo
    app.register_blueprint(form_routes)