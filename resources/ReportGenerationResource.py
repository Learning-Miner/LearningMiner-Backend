from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.db import db
from database.models.ConceptMap import ConceptMap
from database.models.Report import StudentReport
from .Analytics import Analytics
class CreateReportsEndpoint(Resource):
    @jwt_required
    def get(self,baseId):
        user = get_jwt_identity()
        if user['rol'] == 'Student':
            return {"Error" : "Student cannot create reports"}, 401
        students_cms = ConceptMap.objects(baseId=baseId)
        base_cm = ConceptMap.objects(id=baseId)
        analytics = Analytics(students_cms.to_json(),base_cm.to_json())
        ind_reports = analytics.generate_reports()
        self.save_ind_reports(ind_reports)
        return ind_reports
        
    def save_ind_reports(self,ind_reports):
        for ind_report in ind_reports:
            report = StudentReport(**ind_report)
            report.save()

class RetrieveReportsEndpoint(Resource):
    @jwt_required
    def post(self,baseId):
        body = request.get_json()
        if body['query'] == 'group':
            return {"Mesage":"Group Report"}
        if body['query'] == 'student':
            stu_id = body['student_id']
            return {"Mesage":"Student " + stu_id + " report"}
        


