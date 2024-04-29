from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(80))

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
            }
    
class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer)
    climate = db.Column(db.String(80))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "climate": self.climate
            }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.relationship(Planets)
    planetId = db.Column(db.Integer, db.ForeignKey('planets.id'))
    people = db.relationship(People)
    peopleId = db.Column(db.Integer, db.ForeignKey('people.id'))
    user=db.relationship(User)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "planetId": self.planetId,
            "peopleId": self.peopleId,
            "userId": self.userId
            }