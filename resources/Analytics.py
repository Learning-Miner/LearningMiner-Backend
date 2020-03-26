import json
import datetime
from pprint import pprint
class Analytics():
    def __init__(self, students_cms, base_cm):
        self.students_cms = json.loads(students_cms)
        self.base_cm = json.loads(base_cm)

    def advance_ind_reports(self):
        ind_reports = list()
        for std_cm in self.students_cms:
            ind_reports.append(self.process_phase1_std_map(std_cm)) 
        return ind_reports
        

    def advance_grp_report(self):
        pass

    def finish_ind_rerpots(self):
        pass

    def finish_grp_report(self):
        return self.students_cms, self.base_cm

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