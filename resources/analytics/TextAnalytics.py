from numpy import argmax, append
from pandas import DataFrame
import spacy
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

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