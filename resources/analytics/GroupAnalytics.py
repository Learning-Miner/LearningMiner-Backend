from .TextAnalytics import TextAnalytics

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