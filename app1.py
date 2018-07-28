from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key = 'jose'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

#items = []


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register') # когда обращаемся с post запросом по ссылке /register, вызовем класс UserRegister из user.py
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')

# если мы ипортируем app1.py в каком-то из файлов, app1.py будет запускаться и, следовательно,
# запускать flask application, а мы этого не хотим. Поэтому уточняем, что запуск необходим только когда
# app1.py запускается как main
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)
# второй параметр отвечает за explicit описание ошибок
