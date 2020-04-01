from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models.Activity import Activity

class CreateActivityResource(Resource):
    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error":"Student cannot create activity"}, 401
            body = request.get_json()
            act = self.create_activity(body,user['id'])
            act.save()
            return {"act_id":str(act.id)}, 201
        except Exception as e:
            return {'Error': str(e)}, 500

    def create_activity(self,body,uid):
        act = Activity(uid=uid)
        act.dateCreated = datetime.now()
        act.text = body['text']
        act.dateClose = body['dateClose']
        act.title = body['title']
        return act