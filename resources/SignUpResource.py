from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash
from database.models.User import User

class SignupEndpoint(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.password = self.hash_password(user.password)
        user.save()
        id = user.id
        return {'id': str(id)}, 200
    
    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')   