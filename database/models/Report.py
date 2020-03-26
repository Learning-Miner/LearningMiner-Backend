from ..db import db
from .User import User
from .ConceptMap import ConceptMap

class StudentReport(db.Document):
    uid = db.ReferenceField('User')
    baseId = db.ReferenceField('ConceptMap')
    similarity = db.FloatField()
    num_concepts = db.IntField()
    dominant_topic = db.StringField()
    time_used = db.FloatField()

class GroupReport(db.Document):
    baseId = db.ReferenceField('ConceptMap')
    similarity_values = db.ListField(db.FloatField())
    num_concepts_values = db.ListField(db.IntField())
    time_used_values = db.ListField(db.FloatField())
    #topic_model = db.ReferenceField('TopicModel')