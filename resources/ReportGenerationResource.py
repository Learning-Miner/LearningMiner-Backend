from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.db import db
from database.models.ConceptMap import ConceptMap

class CreateReportsEndpoint(Resource):
    @jwt_required
    def get(self,baseId):
        students_cms = ConceptMap.objects(baseId=baseId)
        base_cm = ConceptMap.objects(id=baseId)
        self.advance_ind_reports(students_cms,base_cm)
        self.advance_grp_report(students_cms,base_cm)
        self.finish_ind_rerpots(students_cms,base_cm)
        group_report = self.finish_grp_report(students_cms,base_cm)
        strt = "Base "+str(len(base_cm))+" Stds "+str(len(students_cms))
        return {"mesage":strt}
        
    def advance_ind_reports(self,students_cms,base_cm):
        pass
    
    def advance_grp_report(self,students_cms,base_cm):
        pass

    def finish_ind_rerpots(self,students_cms,base_cm):
        pass

    def finish_grp_report(self,students_cms,base_cm):
        return "Group Report"


class RetrieveReportsEndpoint(Resource):
    @jwt_required
    def post(self,baseId):
        body = request.get_json()
        if body['query'] == 'group':
            return {"Mesage":"Group Report"}
        if body['query'] == 'student':
            stu_id = body['student_id']
            return {"Mesage":"Student " + stu_id + " report"}
        


