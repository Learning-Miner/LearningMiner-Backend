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
    title = db.StringField(required=True)
    isBase = db.BooleanField(required=True)
    dateCreated = db.DateTimeField(required=True)
    dateFinished = db.DateTimeField()
    concepts = db.ListField(db.EmbeddedDocumentField("Concept"))
    propositions = db.ListField(db.EmbeddedDocumentField("Proposition"))
