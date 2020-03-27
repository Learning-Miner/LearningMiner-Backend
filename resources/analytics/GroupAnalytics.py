from .TextAnalytics import TextAnalytics

class GroupAnalytics():
    def __init__(self, students_cms, base_cm,txt_analytics):
        self.students_cms = students_cms
        self.base_cm = base_cm
        self.txt_analytics = txt_analytics

    def advance_grp_report(self):
        docs = self. maps_as_docs()
        self.txt_analytics.build_nmf_topic_model(docs)
        kwt = self.txt_analytics.keywords_topic(docs,10)# Should return json
        cdt = self.txt_analytics.count_docs_topic(docs)# Should return json
        return kwt, cdt
    
    def maps_as_docs(self):
        docs = list()
        for std_cm in self.students_cms:
            text = self.get_cm_string(std_cm)
            docs.append(text)
        return docs

    def get_cm_string(self,std_cm):
        text = ""
        for c in std_cm['concepts']:
            text += " " + c['text'] + " "
        return text