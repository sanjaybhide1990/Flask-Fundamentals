import os, uuid, datetime, pytz
from datetime import datetime
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

IST = pytz.timezone('Asia/Kolkata')

def generate_uuid():
     return str(uuid.uuid4())

class Teams(db.Model):
     __tablename__ = 'teams'

     id = db.Column(db.String(36),primary_key=True,default=generate_uuid,nullable=False)
     name = db.Column(db.Text(30),nullable=False)
     created_at = db.Column(db.DateTime)
     updated_at = db.Column(db.DateTime)

     def __init__(self,name,created_at,updated_at):
          self.name = name
          self.created_at = created_at
          self.updated_at = updated_at
     
     def __repr__(self):
          return f'Team created!! Details ->Name:{self.name} '
class Riders(db.Model):
      __tablename__ = 'riders'

      id = db.Column(db.String(36),primary_key=True,default=generate_uuid,nullable=False)
      name = db.Column(db.Text(30),nullable=False)
      created_at = db.Column(db.DateTime)
      updated_at = db.Column(db.DateTime)
      team_id = db.Column(db.String(36),db.ForeignKey('teams.id'),nullable=False)
      age = db.Column(db.Integer,nullable=False)
      number = db.Column(db.Integer,nullable=False)

      def __init__(self,name,team_id,age,number,created_at,updated_at):
            self.name = name
            self.team_id = team_id
            self.age = age
            self.number = number
            self.created_at = created_at
            self.updated_at = updated_at
      
      def __repr__(self) -> str:
            return f'Rider created!! Details-> Name:{self.name},Team:{self.team},Age:{self.age},Num:{self.number}'

@app.route('/api/addRider',methods=['POST'])
def add_rider():
    riderData = request.get_json()
    checkIfRiderExists = Riders.query.filter_by(number=riderData["number"]).first()
    get_team_id = Teams.query.filter_by(name=riderData["teamName"]).first()
    if get_team_id and not checkIfRiderExists:
        riderToBeAdded = Riders(name=riderData["name"],
                                team_id=get_team_id.id,
                                age=riderData["age"],
                                number=riderData["number"],
                                created_at=datetime.now(IST),
                                updated_at=datetime.now(IST))
        db.session.add(riderToBeAdded)
        db.session.commit()
        return make_response('Rider added successfully',201)
    return make_response('Rider already exists',409)

@app.route('/api/addTeam',methods=['POST'])
def add_team():
     teamData = request.get_json()
     check_if_team_exists = Teams.query.filter_by(name=teamData["name"]).first()
     if not check_if_team_exists:
          team_to_be_added = Teams(name=teamData["name"],created_at=datetime.now(IST),updated_at=datetime.now(IST))
          db.session.add(team_to_be_added)
          db.session.commit()
          return make_response('Team added successfully')
     return make_response('Team already exists')

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