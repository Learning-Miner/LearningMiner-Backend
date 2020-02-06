from flask import request
from flask_restful import Resource
from flask_bcrypt import check_password_hash
from mongoengine.errors import DoesNotExist


from database.models.User import User

class LoginEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')
            user = User.objects.get(email=email)
            authorized = self.check_password(password,user.password)
            if not authorized:
                return {'Error': 'Email or password invalid'}, 401
            return {'Login ok': 123456}, 200
        except DoesNotExist:
            return {'Error': 'Email or password invalid'}, 401
        except Exception:
            return {'Error': 'Something went wrong'}, 500

    def check_password(self,req_pass,usr_pass):
        return check_password_hash(usr_pass,req_pass)