from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User_info(db.Model):
    __tablename__ = "user_info"

    user_id = db.Column(db.String(20), primary_key=True)
    user_password = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password


class Article_list(db.Model):
    __tablename__ = "article_list"

    article_number = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(30))
    article_contents = db.Column(db.Text)
    article_writer = db.Column(db.String(20))
    article_time = db.Column(db.DateTime(timezone=True))

    def __init__(self, article_writer, article_title, article_contents, article_time):
        self.article_writer = article_writer
        self.article_title = article_title
        self.article_contents = article_contents
        self.article_time = article_time

    def __str__(self):
        return '%s %s %s %s' % (self.article_number, self.article_writer, self.article_title, self.article_contents)


class Comment_list(db.Model):
    __tablename__ = "comment_list"

    comment_number = db.Column(db.Integer, primary_key=True)
    comment_contents = db.Column(db.Text)
    comment_writer = db.Column(db.String(20))
    comment_time = db.Column(db.DateTime(timezone=True))
    comment_parent = db.Column(db.Integer)

    def __init__(self, comment_writer, comment_contents, comment_time, comment_parent):
        self.comment_writer = comment_writer
        self.comment_contents = comment_contents
        self.comment_time = comment_time
        self.comment_parent = comment_parent
