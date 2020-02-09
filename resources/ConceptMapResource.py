from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from mongoengine.errors import (
    DoesNotExist, 
    ValidationError, 
    FieldDoesNotExist
)
from database.db import db
from database.models.ConceptMap import (
    ConceptMap, 
    Concept, 
    Proposition
)

class CreateConceptMapEndpoint(Resource):
    @jwt_required
    def post(self):
        try:
            body = request.get_json()
            user = get_jwt_identity()
            if body['isBase'] and user['rol'] == 'Student':
                return {"Error" : "Student cannot create base concept map"}, 401
            ob = ConceptMapUtils()
            cm = ob.create_concept_map(body,user['id'])
            cm.save()
            return {'id': str(cm.id)}, 201
        except ValidationError:
            return {"Error" : "Request is missing required fields"}, 400
        except FieldDoesNotExist:
            return {"Error": "Invalid field"}, 400
        except Exception as e:
            return {'Error': str(e)}, 500

    @jwt_required
    def get(self):
        try:
            user = get_jwt_identity()
            qs = ConceptMap.objects(uid=user['id']).only('title','id')
            cm_titles_ids = [(cm.title, str(cm.id)) for cm in qs]
            if len(cm_titles_ids) == 0:
                return {'Message': 'User does not have created maps'}, 200    
            return cm_titles_ids, 200
        except Exception as e:
            return {'Error': str(e)}, 500
class AlterConceptMapEndpoint(Resource):
    @jwt_required
    def put(self,id):#AKA Save
        try:
            body = request.get_json()
            cm = ConceptMap.objects.get(id=id)
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error" : "Student cannot access base concept map"}, 401
            ob = ConceptMapUtils()
            ob.update_concept_map(body,cm)
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {"Error": str(e)}, 500

    @jwt_required
    def delete(self,id):
        try:
            cm = ConceptMap.objects.get(id=id)
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error" : "Student cannot access base concept map"}, 401
            cm.delete()
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500

    @jwt_required
    def get(self,id):
        try:
            cm = ConceptMap.objects.get(id=id).to_json()
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error" : "Student cannot access base concept map"}, 401
            return Response(cm, mimetype="application/json", status=200)
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500

class ConceptMapUtils():
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

    def create_concept_map(self,body,uid):
        cm = ConceptMap(uid=uid)
        cm.title = body['title']
        if 'concepts' in body.keys():
            cm.concepts = self.create_concept_list(body['concepts'])
        if 'propositions' in body.keys():
            cm.propositions = self.create_propositions_list(body['propositions'])
        cm.isBase = body['isBase']
        cm.dateCreated = datetime.now()
        return cm

    def update_concept_map(self,body,cm):
        if 'concepts' in body.keys():
            concepts = self.create_concept_list(body['concepts'])
            cm.update(set__concepts=concepts)
        if 'propositions' in body.keys():
            propositions = self.create_propositions_list(body['propositions']) 
            cm.update(set__propositions=propositions)            