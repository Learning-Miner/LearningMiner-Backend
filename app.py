from flask import Flask, request, Response
from flask_restful import Api
from resources.routes import initialize_routes
from database.db import initialize_db
from database.connStr import connStr


app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = connStr

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__': 
    app.run(debug=True, port=5000)