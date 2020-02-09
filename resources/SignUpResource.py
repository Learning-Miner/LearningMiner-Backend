from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash
from mongoengine.errors import (
    FieldDoesNotExist, 
    NotUniqueError,  
    ValidationError
)
from database.models.User import User

class SignupEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.password = self.hash_password(user.password)
            user.save()
            id = user.id
            return {'id': str(id)}, 201
        except ValidationError:
            return {"Error" : "Request is missing required fields"}, 400
        except FieldDoesNotExist:
            return {"Error": "Invalid field"}, 400
        except NotUniqueError:
            return {"Error": "User with given email address already exists"}, 400
        except Exception as e:
            return {"Error": str(e)}, 500
    
    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')