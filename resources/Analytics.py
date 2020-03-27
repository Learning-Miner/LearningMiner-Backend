import json
import datetime
from numpy import argmax, append
from pandas import DataFrame
import spacy
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint

class Analytics():
    def __init__(self, students_cms, base_cm):
        students_cms = json.loads(students_cms)
        base_cm = json.loads(base_cm)
        txt_analytics = TextAnalytics()
        self.std_analytics = StudentAnalytics(students_cms,base_cm,txt_analytics)
        self.grp_analytics = GroupAnalytics(students_cms,base_cm,txt_analytics)
    
    def generate_reports(self):
        ind_reports = self.advance_ind_reports()
        kwt, cdt  = self.advance_grp_report()
        kwt = self.serialize_keywords_df(kwt,3)
        pprint(kwt)
        cdt = self.serialize_topic_doc_df(cdt)
        pprint(cdt)
        return ind_reports
        #some method to add dominant topic to each ind_reports
        #some method that contructs group_report json(ind_reports) 
        #return ind_reports, group_report both as json

    def advance_ind_reports(self):
        ind_reports = self.std_analytics.advance_ind_reports()
        return ind_reports
        
    def advance_grp_report(self):
        kwt, cdt = self.grp_analytics.advance_grp_report()
        return kwt, cdt

    def finish_ind_rerpots(self):
        pass

    def finish_grp_report(self):
        return {"Message":"GR"}

    def serialize_keywords_df(self,df,num_topics):
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

    def serialize_topic_doc_df(self,df):
        json = (
            {'topic': df['topic'].to_list(), 
            'student_count': df['student_count'].to_list()}
        )
        return json

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

class TextAnalytics():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.model = None
        self.vectorizer = None
        self.features = None

    def is_valid_token(self,token):
        ret = True
        if token.is_stop:
            ret = False
        if token.pos_ == 'SYM':
            ret = False
        return ret
       
    def preprocess(self,word):
        return str([token.lemma_ for token in self.nlp(word) if self.is_valid_token(token)])
        
    def feature_extraction(self,docs):
        vectorizer = TfidfVectorizer(preprocessor=self.preprocess)
        """vectorizer = TfidfVectorizer( max_df=0.95, 
                                            min_df=2,
                                            preprocessor=self.preprocess )"""
        features = vectorizer.fit_transform(docs)
        return features, vectorizer

    def build_nmf_topic_model(self,docs):
        features, vectorizer = self.feature_extraction(docs)
        nmf_model = NMF(n_components=3)
        nmf_model.fit_transform(features)
        self.model = nmf_model
        self.vectorizer = vectorizer
        self.features = features

    def keywords_topic(self,docs,top_n):
        for i, doc in enumerate(docs):
            docs[i] = self.preprocess(doc)
        as_tuple_list = []
        words = self.vectorizer.get_feature_names()
        for topic_id, importances in enumerate(self.model.components_):
            for word_idx in importances.argsort()[:-top_n - 1:-1]:
                if importances[word_idx] > 0:
                    count = self.count_word_occurance(docs,words[word_idx])
                    row = (words[word_idx], importances[word_idx], topic_id, count)
                    as_tuple_list.append(row)
        df = DataFrame(data=as_tuple_list,columns=['word','importance','topic','count'])
        return df

    def count_word_occurance(self,docs,word):
        count = 0
        for doc in docs:
            count += doc.count(word)
        return count

    def count_docs_topic(self,docs):
        num_topics = 3
        topic_count = []
        
        for doc in docs:
            topics = self.model.transform(self.vectorizer.transform([doc]))[0]
            topic_count.append(int(argmax(topics)))
        
        as_tuple = []
        for topic in range(num_topics):
            count = self.counter(topic,topic_count)
            row = (topic,count)
            as_tuple.append(row)

        df = DataFrame(data=as_tuple,columns=['topic','student_count'])
        return df

    def counter(self,target, arr):
        count = 0
        for i,ele in enumerate(arr):
            if ele == target:
                count += 1
        return count