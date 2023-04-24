import os, uuid
from flask import Flask, request
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
    checkIfRiderExists = Riders.query.filter_by(name=riderData["number"]).first()
    if not checkIfRiderExists:
        riderToBeAdded = Riders(name=riderData["name"],team=riderData["team"],age=riderData["age"],number=riderData["number"])
        db.session.add(riderToBeAdded)
        db.session.commit()
        return 'Rider added successfully'
    return 'Rider already exists'

if __name__ == '__main__':
    app.run()