from ..db import db
from .User import User
from .ConceptMap import ConceptMap

class Activity(db.Document):
    uid = db.ReferenceField('User')
    title = db.StringField(required=True)
    dateCreated = db.DateTimeField(required=True)
    dateClose = db.DateTimeField(required=True)
    text = db.StringField(required=True)
    baseId = db.ReferenceField('ConceptMap')
    key_concepts = db.ListField(db.StringField())
    isClosed = db.BooleanField()
