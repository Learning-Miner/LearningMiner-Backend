from datetime import datetime

from database.models.ConceptMap import Concept, Proposition, ConceptMap


class ConceptMapUtils:
    def create_concept_list(self, json_cpts):
        concepts = list()
        for c in json_cpts:
            new_cpt = Concept(**c)
            concepts.append(new_cpt)
        return concepts

    def create_propositions_list(self, json_prts):
        propositions = list()
        for p in json_prts:
            new_prt = Proposition(**p)
            propositions.append(new_prt)
        return propositions

    def create_concept_map(self, body, uid):
        cm = ConceptMap(uid=uid)
        cm.title = body['title']
        if 'concepts' in body.keys():
            cm.concepts = self.create_concept_list(body['concepts'])
        if 'propositions' in body.keys():
            cm.propositions = self.create_propositions_list(body['propositions'])
        if 'baseId' in body.keys():
            base = ConceptMap.objects.get(id=body['baseId'])
            cm.baseId = base.id
        cm.isBase = body['isBase']
        cm.dateCreated = datetime.now()
        return cm

    def update_concept_map(self, body, cm):
        if 'concepts' in body.keys():
            concepts = self.create_concept_list(body['concepts'])
            cm.update(set__concepts=concepts)
        if 'propositions' in body.keys():
            propositions = self.create_propositions_list(body['propositions'])
            cm.update(set__propositions=propositions)
        if 'isDone' in body.keys():
            cm.update(set__isDone=body['isDone'])