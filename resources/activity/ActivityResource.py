from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models.Activity import Activity
from resources.analytics.Analytics import Analytics
from resources.concept_map.ConceptMapUtils import ConceptMapUtils


class CreateActivityEndpoint(Resource):
    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error": "Student cannot create activity"}, 401
            body = request.get_json()
            analytics = Analytics('act_text', dict({'text': body['text'], 'title': body['title']}))
            key_concepts, base_map_id = self.process_activity_text(analytics, user['id'])
            act = self.create_activity(body, user['id'], key_concepts, base_map_id)
            act.save()
            return {"act_id": str(act.id)}, 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'Error': str(e)}, 500

    def create_activity(self, body, uid, key_concepts, base_map_id):
        act = Activity(uid=uid)
        act.dateCreated = datetime.now()
        act.text = body['text']
        act.dateClose = body['dateClose']
        act.title = body['title']
        act.key_concepts = key_concepts
        act.baseId = base_map_id
        act.isClosed = False
        return act

    def process_activity_text(self, analytics, uid):
        key_concepts, base_map_data = analytics.process_activity_text()
        cmu = ConceptMapUtils()
        base_map = cmu.create_concept_map(base_map_data, uid)
        base_map_id = base_map.save()
        return key_concepts, base_map_id
        
class FilterActivityEndpoint(Resource):
    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            body = request.get_json()
            if body['query'] == 'open':
                open_acts = self.getOpenActivities(user)
                if len(open_acts) == 0:
                    return {'Message': 'User does not have open activities'}, 200
                else:
                    return open_acts
            if body['query'] == 'closed':
                closed_acts = self.getClosedActivities(user)
                if len(closed_acts) == 0:
                    return {'Message': 'User does not have closed activities'}, 200
                else:
                    return closed_acts
        except Exception as e:
            return {'Error': str(e)}, 500

    def getOpenActivities(self,user):
        open_acts = Activity.objects(uid=user['id'],isClosed=False).only('title','baseId')
        ret_acts = [{"Title":act.title,"actId":str(act.id),"baseId":str(act.baseId.id)} for act in open_acts]
        return ret_acts

    def getClosedActivities(self,user):
        closed_acts = Activity.objects(uid=user['id'],isClosed=True).only('title','baseId')
        ret_acts = [{"Title":act.title,"actId":str(act.id),"baseId":str(act.baseId.id)} for act in closed_acts]
        return ret_acts

class EditActivityEndpoint(Resource):
    @jwt_required
    def put(self,actId):
        try:
            user = get_jwt_identity()
            body = request.get_json()
            act = Activity.objects.get(id=actId)
            if str(act.uid.id) == user['id']:
                if 'title' in body.keys():
                    act.update(set__title=body['title'])
                if 'dateClose' in body.keys():
                    act.update(set__dateClose=body['dateClose'])
                if 'isClosed' in body.keys():
                    act.update(set__isClosed=body['isClosed'])
                if 'key_concepts' in body.keys():
                    act.update(set__key_concepts=body['key_concepts'])
                return '', 204
            else:
                return {'Message': 'User is not authorized to edit this activity'}, 401
        except Exception as e:
           return {'Error': str(e)}, 500
    
    @jwt_required
    def get(self,actId):
        try:
            user = get_jwt_identity()
            act = Activity.objects.only('title','key_concepts','dateClose','baseId','uid').get(id=actId)
            if str(act.uid.id) == user['id']:
                print(act.dateClose,type(act.dateClose))
                json = dict()
                json["Title"] = act.title
                json["dateClose"] = str(act.dateClose)
                json["baseId"] = str(act.baseId.id)
                json["key_concepts"] = list(act.key_concepts)
                return json, 200
            else:
                return {'Message': 'User is not authorized to edit this activity'}, 401
        except Exception as e:
           return {'Error': str(e)}, 500