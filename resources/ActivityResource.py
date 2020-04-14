from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models.Activity import Activity
from .analytics.ActivityTextAnalytics import ActivityTextAnalytics
from .ConceptMapResource import ConceptMapUtils

class CreateActivityResource(Resource):
    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error":"Student cannot create activity"}, 401
            body = request.get_json()
            ata = ActivityTextAnalytics(body['text'],body['title'])
            key_concepts, base_map_id = self.process_activity_text(ata,user['id'])
            act = self.create_activity(body,user['id'],key_concepts,base_map_id)
            act.save()
            return {"act_id":str(act.id)}, 201
        except Exception as e:
           return {'Error': str(e)}, 500

    def create_activity(self,body,uid,key_concepts,base_map_id):
        act = Activity(uid=uid)
        act.dateCreated = datetime.now()
        act.text = body['text']
        act.dateClose = body['dateClose']
        act.title = body['title']
        act.key_concepts = key_concepts
        return act

    def process_activity_text(self,analytics,uid):
        key_concepts, base_map_data = analytics.process_activity_text()
        cmu = ConceptMapUtils()
        base_map = cmu.create_concept_map(base_map_data,uid)
        base_map_id = base_map.save()
        return key_concepts, base_map_id