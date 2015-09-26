from flask import Flask, request, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:superpassword@127.0.0.1/testdb"
db = SQLAlchemy(app)


class rawFile(db.Model):
    __tablename__ = "rawFile"
    remoteUrl = db.Column(db.String(300),unique = True)
    shortUrl = db.Column(db.String(300),primary_key = True)
    def __init__(self, url, shortUrl):
        #super(rawFile, self).__init__()
        self.remoteUrl = url
        self.shortUrl = shortUrl


db.create_all()