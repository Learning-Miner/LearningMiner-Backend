from flask import request
from flask_restful import Resource
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
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
            authorized = self.check_password(password, user.password)
            if not authorized:
                return {'Error': 'Email or password invalid'}, 401
            access_token = self.create_jwt_token(user)
            return {'token': access_token, 'rol': user.rol}, 200
        except DoesNotExist:
            return {'Error': 'Email or password invalid'}, 401
        except Exception as e:
            return {'Error': str(e)}, 500

    def check_password(self, req_pass, usr_pass):
        return check_password_hash(usr_pass, req_pass)

    def create_jwt_token(self, usr):
        expires = datetime.timedelta(hours=3)
        idt = {'id': str(usr.id), 'rol': usr.rol}
        access_token = create_access_token(identity=idt, expires_delta=expires)
        return access_token
