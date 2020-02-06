from flask import request
from flask_restful import Resource
from flask_bcrypt import check_password_hash

from database.models.User import User

class LoginEndpoint(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = self.check_password(body.get('password'),user.password)
        if not authorized:
            return {'Error': 'Email or password invalid'}, 401
        return {'Login ok': 123456}, 200

    def check_password(self,req_pass,usr_pass):
        return check_password_hash(req_pass,usr_pass)