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

class Topic(db.EmbeddedDocument):
    topic = db.IntField()
    words = db.ListField(db.StringField())
    importances = db.ListField(db.FloatField())
    counts = db.ListField(db.IntField())

class TopicDocumentCount(db.EmbeddedDocument):
    topic = db.ListField(db.IntField())
    student_count = db.ListField(db.IntField())

class GroupReport(db.Document):
    baseId = db.ReferenceField('ConceptMap')
    similarity_values = db.ListField(db.FloatField())
    num_concepts_values = db.ListField(db.IntField())
    time_used_values = db.ListField(db.FloatField())
    topics = db.ListField(db.EmbeddedDocumentField("Topic"))
    topic_doc_count = db.EmbeddedDocumentField("TopicDocumentCount")