from ..db import db
from .User import User
class Concept(db.EmbeddedDocument):
    text = db.StringField() 
    x = db.IntField()
    y = db.IntField()
    id = db.StringField() 

class Proposition(db.EmbeddedDocument):
    text = db.StringField()
    frm = db.StringField() 
    to = db.StringField()

class ConceptMap(db.Document):
    uid = db.ReferenceField('User')
    baseId = db.ReferenceField('ConceptMap')
    title = db.StringField()
    isBase = db.BooleanField(required=True)
    isGroup = db.BooleanField()
    dateCreated = db.DateTimeField(required=True)
    dateFinished = db.DateTimeField()
    isDone = db.BooleanField()
    concepts = db.ListField(db.EmbeddedDocumentField("Concept"))
    propositions = db.ListField(db.EmbeddedDocumentField("Proposition"))
