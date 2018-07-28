import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                type = str,
                required = True,
                help = 'This field cannot be left blank!'
            )
    parser.add_argument('password',
                type = str,
                required = True,
                help = 'This field cannot be left blank!'
            )

    def post (self):
        # приконнектиться к базе
        # проверить, не существует ли такого юзера
        # считать username и пароль
        # записать данные в БД

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'msg' : 'user already exists'}, 400

        #user = UserModel(data['username'], data['password'])
        user = UserModel(**data) # unpacks dictionary
        user.save_to_db()

        return {"msg" : "user created successfully"}
