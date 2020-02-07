from flask import request
from flask_restful import Resource
from database.db import db
from database.models.ConceptMap import ConceptMap, Concept, Proposition

class ConceptMapEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            cm = self.create_concept_map(body)
            cm.save()
            return {'id': str(cm.id)}, 201
        except Exception as e:
            print(str(e))
            return {'Error': "Failed"}, 500

    def create_concept_list(self,json_cpts):
        concepts = list()
        for c in json_cpts:
            new_cpt = Concept(**c)
            concepts.append(new_cpt)
        return concepts
    
    def create_propositions_list(self,json_prts):
        propositions = list()
        for p in json_prts:
            new_prt = Proposition(**p)
            propositions.append(new_prt)
        return propositions

    def create_concept_map(self,body):
        cm = ConceptMap()
        cm.concepts = self.create_concept_list(body['concepts'])
        cm.propositions = self.create_propositions_list(body['propositions'])
        cm.uid = str(body['uid'])
        cm.isBase = str(body['isBase'])
        cm.dateCreated = str(body['dateCreated'])
        cm.dateFinished = str(body['dateFinished'])
        return cm
        