from flask import Flask
from flask_cors import CORS
from config import create_app
from routes import init_routes

# init server and mongodb
app, mongo = create_app()

# use cors
CORS(app)

# init routes
init_routes(app, mongo)

if __name__ == '__main__':
    app.run(debug=True)
    
