from flask import request
from flask_restful import Resource
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required #Not necessary here
import datetime
from mongoengine.errors import DoesNotExist


from database.models.User import User

class LoginEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')
            if not email or not password:
                return {'Error': 'Email or password missing'}, 401
            user = User.objects.get(email=email)
            authorized = self.check_password(password,user.password)
            if not authorized:
                return {'Error': 'Email or password invalid'}, 401
            access_token = self.create_jwt_token(user.id)
            return {'token': access_token, 'uid': str(user.id)}, 200
        except DoesNotExist:
            return {'Error': 'Email or password invalid'}, 401
        except Exception:
            return {'Error': 'Something went wrong'}, 500

    def check_password(self,req_pass,usr_pass):
        return check_password_hash(usr_pass,req_pass)

    def create_jwt_token(self,usr_id):
        expires = datetime.timedelta(minutes=2)#Update time delta to something useful
        access_token = create_access_token(identity=str(usr_id), expires_delta=expires)
        return access_token
    
    #Mock route to test token
    @jwt_required
    def get(self):
        return {'Cool': 'You have access'}, 200