from .TextAnalytics import TextAnalytics
from random import randint

class GroupAnalytics():
    def __init__(self, students_cms, base_cm,txt_analytics):
        self.students_cms = students_cms
        self.base_cm = base_cm
        self.txt_analytics = txt_analytics

    def advance_grp_report(self):
        docs = self.txt_analytics.maps_as_docs(self.students_cms)
        self.txt_analytics.build_nmf_topic_model(docs)
        kwt = self.txt_analytics.keywords_topic(docs,10)# Should return json
        cdt = self.txt_analytics.count_docs_topic(docs)# Should return json
        return kwt, cdt
    
    def finish_grp_report(self,group_report,ind_reports):
        similarity_values = []
        num_concepts_values = []
        time_used_values = []
        for ind_report in ind_reports:
            similarity_values.append(ind_report['similarity'])
            num_concepts_values.append(ind_report['num_concepts'])
            time_used_values.append(ind_report['time_used'])

        group_report['similarity_values'] = similarity_values
        group_report['num_concepts_values'] = num_concepts_values
        group_report['time_used_values'] = time_used_values

        return group_report

    def generate_group_map(self,key_concepts):
        group_map = self.txt_analytics.generate_group_map(key_concepts,self.students_cms)
        maps = self.map_per_key_concept(group_map,key_concepts)
        return maps

    def map_per_key_concept(self,group_map,key_concepts):
        maps = list()
        for key_concept in key_concepts:
            x = 35
            y = 366
            json_cm = dict()
            json_cm['concepts'] = []
            json_cm['propositions'] = []
            id_gen = 0
            concepts_dict = dict()
            concepts_dict[key_concept] = id_gen
            con_entry = dict()
            con_entry['text'] = key_concept 
            con_entry['id'] = str(id_gen)
            con_entry["x"] = 762
            con_entry["y"] = 111
            json_cm['concepts'].append(con_entry)
            json_cm['title'] = con_entry['text']
            json_cm['isBase'] = False
            id_gen += 1
            for concept in group_map[key_concept]['text']:
                concepts_dict[concept] = id_gen
                con_entry = dict()
                con_entry['text'] = concept
                con_entry['id'] = str(id_gen)
                con_entry["x"] = x + randint(30,50)
                x += 230
                con_entry["y"] = y 
                json_cm['concepts'].append(con_entry)
                id_gen += 1
            for pro,txt in enumerate(group_map[key_concept]['text']):
                pro_entry = dict()
                pro_entry['frm'] = str(0)
                pro_entry['to'] = str(concepts_dict[txt])
                pro_entry['text'] = group_map[key_concept]['propositions'][pro]
                json_cm['propositions'].append(pro_entry)
            maps.append(json_cm)
        return maps