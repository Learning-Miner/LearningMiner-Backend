from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models.Activity import Activity
from .analytics.ActivityTextAnalytics import ActivityTextAnalytics

class CreateActivityResource(Resource):
    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error":"Student cannot create activity"}, 401
            body = request.get_json()
            ata = ActivityTextAnalytics(body['text'])
            key_concepts, base_map_id = self.process_activity_text(ata)
            #act = self.create_activity(body,user['id'],key_concepts,base_map_id)
            #act.save()
            return {"act_id":"yes"}, 201
        except Exception as e:
            return {'Error': str(e)}, 500

    def create_activity(self,body,uid,key_concepts,base_map_id):
        act = Activity(uid=uid)
        act.dateCreated = datetime.now()
        act.text = body['text']
        act.dateClose = body['dateClose']
        act.title = body['title']
        return act

    def process_activity_text(self,analytics):
        key_concepts, base_map = analytics.process_activity_text()
        print(key_concepts)
        print(base_map)
        #Create and save base map
        base_map_id = 1 #base_map.save()
        return key_concepts, base_map_id