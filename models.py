from flask_sqlalchemy import SQLAlchemy
from schemas import WebtoonSchema 
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1500), unique=True, nullable=False)
    password = db.Column(db.String(1500), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)




class Webtoon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    characters = db.Column(db.ARRAY(db.String), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'characters': self.characters
        }
    

# Initialize your schema
webtoon_schema = WebtoonSchema()
webtoons_schema = WebtoonSchema(many=True)    
