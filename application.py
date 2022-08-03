from enum import unique
from flask import Flask
# from sqlalchemy import null
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello'

@app.route('/fruits')    
def get_fruits():

    fruits = Fruit.query.all()

    output = []
    for fruit in fruits:
        fruit_data = {'name':fruit.name, 'description':fruit.description}

        output.append(fruit_data)

    return{"fruits":output}