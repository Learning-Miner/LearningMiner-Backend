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
        return act

    def process_activity_text(self, analytics, uid):
        key_concepts, base_map_data = analytics.process_activity_text()
        cmu = ConceptMapUtils()
        base_map = cmu.create_concept_map(base_map_data, uid)
        base_map_id = base_map.save()
        return key_concepts, base_map_id
        
class RetrieveReportsEndpoint(Resource):
    @jwt_required
    def post(self,baseId):
        try:
            body = request.get_json()
            user = get_jwt_identity()
            if body['query'] == 'group':
                grp_report = GroupReport.objects(baseId=baseId)
                return json.loads(grp_report.to_json()), 200
            if body['query'] == 'student':
                if user['rol'] == 'Teacher':
                    std_id = body['student_id']
                    std_report = StudentReport.objects(baseId=baseId,uid=std_id)
                    return json.loads(std_report.to_json()), 200
                elif user['rol'] == 'Student':
                    std_report = StudentReport.objects(baseId=baseId,uid=user['id'])
                    return json.loads(std_report.to_json()), 200
                else:
                    return {"Error" : "Student cannot access this student report"}, 401
        except Exception as e:
            return {'Error': str(e)}, 500 
            
    
    @jwt_required
    def get(self,baseId):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error" : "Student cannot access student's reports"}, 401
            std_reports = StudentReport.objects(baseId=baseId).only("uid")
            names_reports = list()
            for report_data in std_reports:
                std = User.objects.only("name","lastname").get(id=report_data.uid.id)
                name = std.name
                lastname = std.lastname
                entry = {"std_name": f'{name} {lastname}', "std_id":str(std.id)}
                names_reports.append(entry)
            return names_reports, 200
        except Exception as e:
            return {'Error': str(e)}, 500 