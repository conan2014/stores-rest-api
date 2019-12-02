from db import db

class ItemModel(db.Model):  # get ItemModel to extend db.Model
                            # i.e. tell SQLAlchemy to create that mapping between database and ItemModel object
    __tablename__ = "items" # Tell SQLAlchemy which table ItemModel is going to be stored at

    id = db.Column(db.Integer, primary_key=True)  # having an id is very useful, even though it doesn't exist in __init__
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel') # this line allows SQLAlchemy to retrieve a StoreModel object
                                          # with id matching the store_id property defined in the ItemModel here
                                          # With this line, you can do item.store and that gives you the StoreModel.
                                          # Without this line, you cannot do this



    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


