from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models.ConceptMap import ConceptMap
from database.models.Report import StudentReport, Topic, TopicDocumentCount, GroupReport
from database.models.User import User
from database.models.Activity import Activity
from resources.analytics.Analytics import Analytics
from resources.concept_map.ConceptMapUtils import ConceptMapUtils
import json
from mongoengine.errors import (
    DoesNotExist, 
    ValidationError, 
    FieldDoesNotExist
)


class CreateReportsEndpoint(Resource):
    @jwt_required
    def get(self,baseId):
        try:
            user = get_jwt_identity()
            if user['rol'] == 'Student':
                return {"Error" : "Student cannot create reports"}, 401
            students_cms = ConceptMap.objects(baseId=baseId)
            base_cm = ConceptMap.objects().get(id=baseId)
            key_concepts = Activity.objects.only("key_concepts").get(baseId=baseId)
            key_concepts = list(key_concepts.key_concepts)
            analytics = Analytics('reports', dict({'students_cms': students_cms.to_json(), 'base_cm': base_cm.to_json()}))
            ind_reports, group_report = analytics.generate_reports()
            self.save_ind_reports(ind_reports)
            gp_maps = analytics.generate_group_maps(key_concepts)
            gp_id = self.save_group_report(group_report,baseId,gp_maps,user['id'])
            return {"Group report id":gp_id}
        except ValidationError:
            return {"Error" : "Request is missing required fields"}, 400
        except FieldDoesNotExist:
            return {"Error": "Invalid field"}, 400
        except DoesNotExist: 
            return {"Error": "Concept map not found"}, 404
        except Exception as e:
            return {'Error': str(e)}, 500     
        
    def save_ind_reports(self,ind_reports):
        for ind_report in ind_reports:
            report = StudentReport(**ind_report)
            report.save()

    def save_group_report(self,group_report,baseId,gp_maps,teacher_id):
        gp = GroupReport(baseId=baseId)
        topics = self.create_topic_list(group_report['topic_keywords'])
        topic_doc_count = TopicDocumentCount(**group_report['topic_doc_count'])
        gp.topic_doc_count = topic_doc_count
        gp.topics = topics
        gp.similarity_values = group_report['similarity_values']
        gp.time_used_values = group_report['time_used_values']
        gp.num_concepts_values = group_report['num_concepts_values']
        utils = ConceptMapUtils()
        gp_maps_ids = list()
        for cm in gp_maps:
            cm = utils.create_concept_map(cm,teacher_id)
            cm.isGroup = True
            cm.save()
            gp_maps_ids.append(cm.id)            
        gp.group_maps = gp_maps_ids
        gp.save()
        return str(gp.id)

    def create_topic_list(self,topics):
        topics_list = list()
        for item in topics['topics']:
            topic_item = Topic(**item)
            topics_list.append(topic_item)
        return topics_list

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
                std_id = body['student_id']
                if user['rol'] == 'Teacher':
                    std_report = StudentReport.objects(baseId=baseId,uid=std_id)
                    return json.loads(std_report.to_json()), 200
                elif user['rol'] == 'Student' and user['id'] == std_id:
                    std_report = StudentReport.objects(baseId=baseId,uid=std_id)
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