import json
from resources.analytics.StudentAnalytics import StudentAnalytics
from resources.analytics.GroupAnalytics import GroupAnalytics
from resources.analytics.ActivityTextAnalytics import ActivityTextAnalytics
from resources.analytics.TextAnalytics import TextAnalytics


class Analytics:
    def __init__(self, analytics_type, data):
        txt_analytics = TextAnalytics()
        if analytics_type == 'reports':
            if 'students_cms' in data.keys():
                students_cms = json.loads(data['students_cms'])
            if 'base_cm' in data.keys():
                base_cm = json.loads(data['base_cm'])                
            self.std_analytics = StudentAnalytics(students_cms, base_cm, txt_analytics)
            self.grp_analytics = GroupAnalytics(students_cms, base_cm, txt_analytics)
        if analytics_type == 'act_text':
            if 'text' in data.keys() and 'title' in data.keys():
                self.act_analytics = ActivityTextAnalytics(data['text'], data['title'], txt_analytics)

    def generate_reports(self):
        ind_reports = self.advance_ind_reports()
        group_report = self.advance_grp_report()
        ind_reports = self.finish_ind_reports(ind_reports)
        group_report = self.finish_grp_report(group_report, ind_reports)
        return ind_reports, group_report

    def advance_ind_reports(self):
        ind_reports = self.std_analytics.advance_ind_reports()
        return ind_reports

    def advance_grp_report(self):
        kwt, cdt = self.grp_analytics.advance_grp_report()
        group_report = dict()
        kwt = self.serialize_keywords_df(kwt, 3)
        cdt = self.serialize_topic_doc_df(cdt)
        group_report['topic_keywords'] = kwt
        group_report['topic_doc_count'] = cdt
        return group_report

    def finish_ind_reports(self, ind_reports):
        return self.std_analytics.finish_ind_reports(ind_reports)

    def finish_grp_report(self, group_report, ind_reports):
        return self.grp_analytics.finish_grp_report(group_report, ind_reports)

    def serialize_keywords_df(self, df, num_topics):
        json = {'topics': list()}
        for idx in range(num_topics):
            topic_json = {}
            topic_json['topic'] = idx
            data = df[df.topic == idx]
            topic_json['words'] = data['word'].to_list()
            topic_json['importances'] = data['importance'].to_list()
            topic_json['counts'] = data['count'].to_list()
            json['topics'].append(topic_json)
        return json

    def serialize_topic_doc_df(self, df):
        json = (
            {'topic': df['topic'].to_list(),
             'student_count': df['student_count'].to_list()}
        )
        return json

    def generate_group_maps(self, key_concepts):
        maps = self.grp_analytics.generate_group_map(key_concepts)
        return maps

    def process_activity_text(self):
        return self.act_analytics.process_activity_text()
