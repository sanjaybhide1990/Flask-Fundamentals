import os, uuid
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sanjay123@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

def generate_uuid():
     return str(uuid.uuid4())

class Riders(db.Model):
      __tablename__ = 'riders'

      id = db.Column(db.String(36),primary_key=True,default=generate_uuid,nullable=False)
      name = db.Column(db.Text(30),nullable=False)
      team = db.Column(db.Text(50),nullable=False)
      age = db.Column(db.Integer,nullable=False)
      number = db.Column(db.Integer,nullable=False)

      def __init__(self,name,team,age,number):
            self.name = name
            self.team = team
            self.age = age
            self.number = number
      
      def __repr__(self) -> str:
            return f'Rider created!! Details-> Name:{self.name},Team:{self.team},Age:{self.age},Num:{self.number}'

@app.route('/api/addRider',methods=['POST'])
def add_rider():
    riderData = request.get_json()
    checkIfRiderExists = Riders.query.filter_by(number=riderData["number"]).first()
    if not checkIfRiderExists:
        riderToBeAdded = Riders(name=riderData["name"],team=riderData["team"],age=riderData["age"],number=riderData["number"])
        db.session.add(riderToBeAdded)
        db.session.commit()
        return make_response('Rider added successfully',201)
    return make_response('Rider already exists',409)

@app.route('/api/updateRider/<number_of_rider>',methods=['PUT'])
def update_rider(number_of_rider):
     riderData = request.get_json()
     check_if_rider_exists = Riders.query.filter_by(number=number_of_rider).first()
     if check_if_rider_exists:
        rider_to_be_updated = Riders.query.get(check_if_rider_exists.id)
        rider_to_be_updated.name = riderData["name"]
        rider_to_be_updated.age = riderData["age"]
        rider_to_be_updated.team = riderData["team"]
        rider_to_be_updated.number = riderData["number"]
        db.session.add(rider_to_be_updated)
        db.session.commit()
        return make_response('Updated successfully',200)
     return make_response('Rider not found',404)  

@app.route('/api/getRider/<number_of_rider>')
def get_rider_info(number_of_rider):
     checkIfRiderExists = Riders.query.filter_by(number=number_of_rider).first()
     if checkIfRiderExists:
        riderObj = {
             "name": checkIfRiderExists.name,
             "number": checkIfRiderExists.number,
             "age": checkIfRiderExists.age,
             "team": checkIfRiderExists.team
        }
        return make_response(riderObj,200)
     return make_response('Rider not found',404)

@app.route('/api/deleteRider/<number_of_rider>',methods=['DELETE'])
def delete_rider(number_of_rider):
     check_if_rider_exists = Riders.query.filter_by(number=number_of_rider).first()
     if check_if_rider_exists:
          rider_to_be_deleted = Riders.query.get(check_if_rider_exists.id)
          db.session.delete(rider_to_be_deleted)
          db.session.commit()
          return make_response('Deleted successfully',200)
     return make_response('Rider not found',404)
          

if __name__ == '__main__':
    app.run()