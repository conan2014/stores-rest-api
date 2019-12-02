from db import db

class UserModel(db.Model):  # get UserModel to extend db.Model
                            # tell SQLAlchemy to create the mapping between database and UserModel object
    __tablename__ = "users" # Tell SQLAlchemy which table UserModel is going to be stored at

    id = db.Column(db.Integer, primary_key=True) # when saving to database, SQLAlchemy is only going to look at those 3 properties
    username = db.Column(db.String(80))          # self.id, self.username, self.password must match the variables on the left
    password = db.Column(db.String(80))          # for them to be saved into the database

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

