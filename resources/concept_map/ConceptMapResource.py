from datetime import datetime
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from .ConceptMapUtils import ConceptMapUtils
from mongoengine.errors import (
    DoesNotExist,
    ValidationError,
    FieldDoesNotExist
)
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
                return {"Error": "Student cannot create base concept map"}, 401
            ob = ConceptMapUtils()
            cm = ob.create_concept_map(body, user['id'])
            cm.save()
            return {'id': str(cm.id)}, 201
        except ValidationError:
            return {"Error": "Request is missing required fields"}, 400
        except FieldDoesNotExist:
            return {"Error": "Invalid field"}, 400
        except Exception as e:
            return {'Error': str(e)}, 500


class FilterUserConceptMapsEndpoint(Resource):
    @jwt_required
    def post(self):
        try:
            body = request.get_json()
            user = get_jwt_identity()
            if body['query'] == 'to-do':
                to_do_cms = self.getToDoMaps(user)
                if len(to_do_cms) == 0:
                    return {'Message': 'User does not have to do maps'}, 200
                else:
                    return to_do_cms
            if body['query'] == 'edit':
                edit_maps = self.getEditMaps(user)
                if len(edit_maps) == 0:
                    return {'Message': 'User does not have created maps'}, 200
                else:
                    return edit_maps
            if body['query'] == 'done':
                done_maps = self.getDoneMaps(user)
                if len(done_maps) == 0:
                    return {'Message': 'User does not have done maps'}, 200
                else:
                    return done_maps
        except Exception as e:
            return {'Error': str(e)}, 500

    def getToDoMaps(self, user):
        base_cms = ConceptMap.objects(isBase=True).only('title', 'id')
        base_cm_titles_ids = [(str(cm.id), cm.title) for cm in base_cms]
        base_cm_titles_ids = dict(base_cm_titles_ids)
        user_cms = ConceptMap.objects(uid=user['id']).only('title', 'id', 'baseId')
        base_ids, user_ids = set(base_cm_titles_ids.keys()), set([str(cm.baseId.id) for cm in user_cms])
        to_do_cms = base_ids - user_ids
        to_do_cms = {k: v for (k, v) in base_cm_titles_ids.items() if k in to_do_cms}
        json = list()
        for id, title in to_do_cms.items():
            entry = {"baseId": id, "title": title}
            json.append(entry)
        return json

    def getEditMaps(self, user):
        user_cms = ConceptMap.objects(uid=user['id']).only('title', 'id', 'isDone', 'baseId')
        user_cm_titles_ids = [(str(cm.id), cm.title, str(cm.baseId.id)) for cm in user_cms if not cm.isDone]
        json = list()
        for cm_data in user_cm_titles_ids:
            entry = {"id": cm_data[0], "title": cm_data[1], "baseId": cm_data[2]}
            json.append(entry)
        return json

    def getDoneMaps(self, user):
        user_cms = ConceptMap.objects(uid=user['id'], isDone=True).only('title', 'id', 'baseId')
        user_cm_titles_ids = [(str(cm.id), cm.title, str(cm.baseId.id)) for cm in user_cms]
        json = list()
        for map_data in user_cm_titles_ids:
            entry = {"id": map_data[0], "title": map_data[1], "baseId": map_data[2]}
            json.append(entry)
        return json


class AlterConceptMapEndpoint(Resource):
    @jwt_required
    def put(self, id):  # AKA Save
        try:
            body = request.get_json()
            cm = ConceptMap.objects.get(id=id)
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error": "Student cannot access base concept map"}, 401
            ob = ConceptMapUtils()
            ob.update_concept_map(body, cm)
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {"Error": str(e)}, 500

    @jwt_required
    def delete(self, id):
        try:
            cm = ConceptMap.objects.get(id=id)
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error": "Student cannot access base concept map"}, 401
            cm.delete()
            return '', 204
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500

    @jwt_required
    def get(self, id):
        try:
            cm = ConceptMap.objects.only('concepts', 'propositions', 'isBase').get(id=id)
            user = get_jwt_identity()
            if cm.isBase and user['rol'] == 'Student':
                return {"Error": "Student cannot access base concept map"}, 401
            return Response(cm.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            return {'Error': 'Invalid ConceptMap id'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500
