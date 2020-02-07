from ..db import db

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
    uid = db.StringField(required=True)
    isBase = db.StringField(required=True)
    dateCreated = db.StringField()
    dateFinished = db.StringField()
    concepts = db.ListField(db.EmbeddedDocumentField("Concept"))
    propositions = db.ListField(db.EmbeddedDocumentField("Proposition"))
