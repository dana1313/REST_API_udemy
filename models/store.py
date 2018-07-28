from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic') # many to one relationship
    # если не написать lazy='dynamic', то каждый раз, когда будет создаваться магазин, будет создаваться связь, что затратно по ресурсам
    #  с ним обращение в таблицу будет только при вызове json()
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name' : self.name, 'items' : [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM __tablename__ WHERE name = name LIMIT 1
        # returns ItemModel object

    def save_to_db(self):
        db.session.add(self) # то, что будет записано в БД
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
