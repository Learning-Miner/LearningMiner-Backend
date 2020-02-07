from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from database.db import db
from database.models.ConceptMap import ConceptMap, Concept, Proposition

class CreateConceptMapEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            ob = ObjectBuilder()
            cm = ob.create_concept_map(body)
            cm.save()
            return {'id': str(cm.id)}, 201
        except Exception as e:
            print(str(e))
            return {'Error': "Failed"}, 500
        
class AlterConceptMapEndpoint(Resource):
    def put(self,id):#AKA Save
        try:
            body = request.get_json()
            ob = ObjectBuilder()
            concepts = ob.create_concept_list(body['concepts'])
            propositions = ob.create_propositions_list(body['propositions']) 
            (ConceptMap.objects(id=id) 
            .only('concepts','propositions')
            .first() 
            .update(set__concepts=concepts,set__propositions=propositions))
            return '', 204
        except Exception as e:
            print(str(e))
            return {'Error': "Failed"}, 500

    def delete(self,id):
        ConceptMap.objects.get(id=id).delete()
        return '', 204

    def get(self,id):
        cm = ConceptMap.objects.get(id=id).to_json()
        return Response(cm, mimetype="application/json", status=200)

class ObjectBuilder():
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
        cm = ConceptMap(uid=body['uid'])
        cm.concepts = self.create_concept_list(body['concepts'])
        cm.propositions = self.create_propositions_list(body['propositions'])
        cm.isBase = body['isBase']
        cm.dateCreated = datetime.now()
        return cm