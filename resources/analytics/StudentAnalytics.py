import datetime
from .TextAnalytics import TextAnalytics

class StudentAnalytics():
    def __init__(self, students_cms, base_cm,txt_analytics):
        self.students_cms = students_cms
        self.base_cm = base_cm
        self.txt_analytics = txt_analytics

    def advance_ind_reports(self):
        ind_reports = list()
        for std_cm in self.students_cms:
            ind_reports.append(self.process_phase1_std_map(std_cm)) 
        return ind_reports

    def process_phase1_std_map(self,std_cm):
        report = dict()
        report['uid'] = std_cm['uid']['$oid']
        report['baseId'] = std_cm['baseId']['$oid']
        report['num_concepts'] = len(std_cm['concepts'])
        report['similarity'] = self.compute_similarity(self.base_cm,std_cm)
        report['time_used'] = self.compute_time_used(std_cm['dateCreated'],std_cm['dateFinished'])
        return report

    def compute_similarity(self,base_cm,cm):
        return 100

    def compute_time_used(self,dateCreated,dateFinished):
        dateCreated = datetime.datetime.fromtimestamp(dateCreated['$date']/1000)
        dateFinished = datetime.datetime.fromtimestamp(dateFinished['$date']/1000)
        dif = dateFinished - dateCreated
        time_used = divmod(dif.seconds, 60)[0]
        return time_used

    def finish_ind_reports(self,ind_reports):
        for idx,ind_report in enumerate(ind_reports):
            topic_ids, importances = self.txt_analytics.topics_per_document(self.students_cms[idx])
            ind_reports[idx]['topic_distribution'] = {"topic":topic_ids,"importances":importances}
        return ind_reports