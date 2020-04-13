from .TextAnalytics import TextAnalytics
from random import randint
class ActivityTextAnalytics:
    def __init__(self,text):
        self.text = text
        self.text_analytics = TextAnalytics()
    
    def process_activity_text(self):
        base_map = self.text_analytics.generate_base_map(self.text)
        key_concepts = base_map.keys()
        base_map = self.base_map_json(base_map)
        return key_concepts, base_map

    def base_map_json(self,base_map):
        id_gen = 1
        json = dict()
        json['concepts'] = list()
        json['propositions'] = list()
        for key,val in base_map.items():
            concept_entry = dict()
            concept_entry['text'] = key
            concept_entry['id'] = id_gen
            concept_entry['x'] = randint(300,1370)
            concept_entry['y'] = randint(142,624)
            json['concepts'].append(concept_entry)
            id_gen += 1
            for v in val:
                concept_entry_2 = dict()
                concept_entry_2['text'] = v
                concept_entry_2['id'] = id_gen
                concept_entry_2['x'] = concept_entry['x'] + randint(100,150)
                concept_entry_2['y'] = concept_entry['y'] + randint(100,150)
                json['concepts'].append(concept_entry_2)
                id_gen += 1
                prop_entry = dict()
                prop_entry['from'] = concept_entry['id']
                prop_entry['to'] = concept_entry_2['id']
                prop_entry['text'] = ""
                json['propositions'].append(prop_entry)
            
        return json