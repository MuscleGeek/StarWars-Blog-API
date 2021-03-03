from flask_sqlalchemy import SQLAlchemy
# import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# from eralchemy import render_er
db = SQLAlchemy()

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "gender":self.gender,
            "email":self.email,
            "favorites":list(map(lambda f: f.serialize(), self.favorites))   
        }

class Favorites(db.Model):
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    type= db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))   

    def serialize(self):
        return{   
            "id": self.id, 
            "name":self.name,
            "type":self.type,     
        }

class People(db.Model):
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    skin_color = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Float, nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "height":self.height,
            "birth_year":self.birth_year,
            "gender":self.gender,
            "image":self.image
        }
    
class Planet(db.Model):
    
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    diameter= db.Column(db.Float, nullable=False)
    climate= db.Column(db.String(200), nullable=False)
    terrain= db.Column(db.String(200), nullable=False)
    population= db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "diameter":self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }
        


