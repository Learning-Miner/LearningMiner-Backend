from flask import Flask, request, Response
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.routes import initialize_routes
from database.db import initialize_db
from database.connStr import connStr


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.config['MONGODB_SETTINGS'] = connStr
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__': 
    app.run(debug=True, port=5000)