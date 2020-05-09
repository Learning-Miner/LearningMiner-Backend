from numpy import argmax, append, array
from pandas import DataFrame
import spacy
import pytextrank
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter, defaultdict

class TextAnalytics():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.model = None
        self.vectorizer = None
        self.features = None

    def maps_as_docs(self,students_cms):
        docs = list()
        for std_cm in students_cms:
            text = self.get_cm_string(std_cm)
            docs.append(text)
        return docs

    def get_cm_string(self,std_cm):
        text = ""
        for c in std_cm['concepts']:
            text += " " + c['text'] + " "
        return text

    def is_valid_token(self,token):
        ret = True
        if token.is_stop:
            ret = False
        if token.pos_ == 'SYM':
            ret = False
        if token.pos_ == 'PUNCT':
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

    def topics_per_document(self,cm):
        doc= self.get_cm_string(cm)
        importances = list()
        topic_ids = list()
        topics = self.model.transform(self.vectorizer.transform([doc]))[0]
        for topic_id, topic_impo in enumerate(topics):
            importances.append(topic_impo)
            topic_ids.append(topic_id)
        return topic_ids, importances

    def is_similar(self,sentence1,sentence2,threshold):
        if sentence1.similarity(sentence2) >= threshold:
            return True
        return False

    def clean_group_map(self,group_map):
        for k,v in group_map.items():
            i = 0
            while i<len(v['text']):
                j = i + 1
                while j<len(v['text']):
                    if self.is_similar(self.nlp(v['text'][i]),self.nlp(v['text'][j]),0.7):
                        del v['text'][j]
                        del v['propositions'][j]
                    j+=1
                i+=1
            group_map[k] = v
        return group_map

    def preprocess_sentence(self,sentence):
        return " ".join([token.lemma_ for token in self.nlp(sentence) if self.is_valid_token(token)]).lower()

    def process_map_for_group_map(self,group_map,cm):
        concepts = dict()
        for con in cm['concepts']:
            concepts[con['id']] = con['text']
        for kc in group_map.keys():
            text = list()
            prop = list()
            key_concept = self.nlp(kc)
            for c in concepts.values():
                c = self.nlp(self.preprocess_sentence(c))
                if self.is_similar(key_concept,c,0.89):
                    for pro in cm['propositions']:
                        pro_txt = self.nlp(self.preprocess_sentence(concepts[pro['frm']]))
                        if self.is_similar(pro_txt,c,0.89):
                            prop.append(pro['text'])
                            text.append(concepts[pro['to']])
            group_map[kc]["propositions"] = group_map[kc]["propositions"] + prop
            group_map[kc]["text"] = group_map[kc]["text"] + text
        return group_map


    def generate_group_map(self,key_concepts,students_cms):
        print(key_concepts)
        for i,c in enumerate(key_concepts):
            key_concepts[i] = self.preprocess_sentence(c)
        
        group_map = dict()
        
        for kc in key_concepts:
            group_map[kc] = {"propositions": list(), "text": list()}

        for cm in students_cms:
            group_map = self.process_map_for_group_map(group_map,cm)    
            
        group_map = self.clean_group_map(group_map)
        return group_map         
    
    def get_key_phrases(self,doc,top_n):
        aux_phrases = []

        aux_phrases.append(self.filter_phrases_by_num_words(2,doc._.phrases))
        aux_phrases.append(self.filter_phrases_by_num_words(3,doc._.phrases))
        aux_phrases.append(self.filter_phrases_by_num_words(4,doc._.phrases))
        
        for idx,phrases in enumerate(aux_phrases):
            if len(phrases) > top_n:
                aux_phrases[idx] = phrases[:top_n]
        
        return aux_phrases

    def filter_phrases_by_num_words(self,num_words,phrases):
        key_phrases = [self.nlp(p.text) for p in phrases if len(self.nlp(p.text)) == num_words and p.rank > 0.05 ]
        return key_phrases

    def cluster_texts(self,docs,num_clusters):
        features, vectorizer = self.feature_extraction(docs)
        km_model = KMeans(n_clusters=num_clusters)
        km_model.fit(features)
        clustering = defaultdict(list)
    
        for idx, label in enumerate(km_model.labels_):
            clustering[label].append(idx)
    
        return clustering

    def process_key_phrases(self,aux_key):
        key_phrases = []
        for phrases in aux_key:
            key_phrases = key_phrases + phrases
        return key_phrases

    def generate_base_map(self,text):
        tr = pytextrank.TextRank()
        self.nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)
        doc = self.nlp(text.lower())
        aux_key = self.get_key_phrases(doc,10)
        key_phrases = self.process_key_phrases(aux_key)
        key = [str(word) for word in key_phrases]

        clus = self.cluster_texts(key,int(len(key[0])/2))
        key = array(key)

        base_map = dict()
        for label, indexs in clus.items():
            if len(key[indexs].tolist()) > 1:
                base_map[key[indexs][0]] = key[indexs].tolist()[1:]
                
        return base_map

    def compute_similarity(self,base_cm,cm):
        base = self.nlp(self.get_cm_string(base_cm))
        std = self.nlp(self.get_cm_string(cm))
        return base.similarity(std)