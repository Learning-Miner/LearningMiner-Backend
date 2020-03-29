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
    
    