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
        students_cms = ConceptMap.objects(baseId=baseId)
        base_cm = ConceptMap.objects(id=baseId)
        analytics = Analytics(students_cms.to_json(),base_cm.to_json())
        self.advance_ind_reports(analytics)
        self.advance_grp_report(analytics)
        self.finish_ind_rerpots(analytics)
        group_report, grp_report = self.finish_grp_report(analytics)
        return {"std":group_report,"base":grp_report}
        
    def advance_ind_reports(self,analytics):
        ind_reports = analytics.advance_ind_reports()
        for ind_report in ind_reports:
            report = StudentReport(**ind_report)
            report.save()

    
    def advance_grp_report(self,analytics):
        analytics.advance_grp_report()

    def finish_ind_rerpots(self,analytics):
        analytics.finish_ind_rerpots()

    def finish_grp_report(self,analytics):
        return analytics.finish_grp_report()


class RetrieveReportsEndpoint(Resource):
    @jwt_required
    def post(self,baseId):
        body = request.get_json()
        if body['query'] == 'group':
            return {"Mesage":"Group Report"}
        if body['query'] == 'student':
            stu_id = body['student_id']
            return {"Mesage":"Student " + stu_id + " report"}
        


