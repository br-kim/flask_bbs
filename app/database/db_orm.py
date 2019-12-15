from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_info(db.Model):
    __tablename__ = "user_info"

    user_id = db.Column(db.String(20), primary_key=True)
    user_password = db.Column(db.String(20), nullable=False)

    def __init__(self,user_id,user_password):
        self.user_id = user_id
        self.user_password = user_password

class User_article(db.Model) :
    __tablename__ = "user_article"

    user_id =  db.Column(db.String(20))
    user_article_number = db.Column(db.Integer,primary_key=True)

class Article_list(db.Model) :
    __tablename__ = "article_list"

    article_number = db.Column(db.Integer,primary_key=True)
    article_contents = db.Column(db.Text)
    def __repr__(self):
        return '%s %s'%(self.article_number,self.article_contents)
    def __iter__(self):
        return self