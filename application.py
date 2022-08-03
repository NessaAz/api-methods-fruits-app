from crypt import methods
from enum import unique
from flask import Flask, jsonify, request
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

@app.route('/fruits/<id>')    
def get_fruit(id):

    fruit = Fruit.query.get_or_404(id)

    return {"name":fruit.name, "description":fruit.description}
    #return jsonify if not working with a dictionary.
    #we don't use it here since dictionaries are serializable

@app.route('/fruits', methods=['POST'])    
def add_fruit():
    fruit = Fruit(name=request.json['name'], description=request.json['description'])

    db.session.add(fruit)
    db.session.commit()

    return {'id': fruit.id }

@app.route('/fruits/<id>', methods=['DELETE'])
def delete_fruit(id):
    fruit = Fruit.query.get(id)

    if fruit is None:
        return{'error':'not found'}

    db.session.delete(fruit)        
    db.session.commit()

    return{'message':'success'}