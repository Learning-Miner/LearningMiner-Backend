from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError, FieldDoesNotExist
from database.db import db
from database.models.ConceptMap import ConceptMap, Concept, Proposition

class CreateConceptMapEndpoint(Resource):
    def post(self):
        try:
            body = request.get_json()
            ob = ConceptMapBuilder()
            cm = ob.create_concept_map(body)
            cm.save()
            return {'id': str(cm.id)}, 201
        except ValidationError:
            return {"Error" : "Request is missing required fields"}, 400
        except FieldDoesNotExist:
            return {"Error": "Invalid field"}, 400
        except Exception as e:
            return {'Error': str(e)}, 500
        
class AlterConceptMapEndpoint(Resource):
    def put(self,id):#AKA Save
        try:
            body = request.get_json()
            ob = ConceptMapBuilder()
            if 'concepts' in body.keys() and 'propositions' in body.keys():
                concepts = ob.create_concept_list(body['concepts'])
                propositions = ob.create_propositions_list(body['propositions']) 
                (ConceptMap.objects(id=id) 
                .only('concepts','propositions')
                .first() 
                .update(set__concepts=concepts,set__propositions=propositions))
            elif 'propositions' in body.keys():
                propositions = ob.create_propositions_list(body['propositions']) 
                (ConceptMap.objects(id=id) 
                .only('propositions')
                .first() 
                .update(set__propositions=propositions))
            else:
                concepts = ob.create_concept_list(body['concepts'])
                (ConceptMap.objects(id=id) 
                .only('concepts')
                .first() 
                .update(set__concepts=concepts))               
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {"Error": "Something went wrong"}, 500

    def delete(self,id):
        try:
            ConceptMap.objects.get(id=id).delete()
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception:
            return {'Error': "Something went wrong"}, 500

    def get(self,id):
        try:
            cm = ConceptMap.objects.get(id=id).to_json()
            return Response(cm, mimetype="application/json", status=200)
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception:
            return {'Error': "Something went wrong"}, 500

class ConceptMapBuilder():
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