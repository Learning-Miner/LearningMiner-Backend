from ..db import db
class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    name = db.StringField(required=True)
    lastname = db.StringField(required=True)
    password = db.StringField(required=True, min_length=6)
    rol = db.StringField(required=True)