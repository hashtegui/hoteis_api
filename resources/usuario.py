from flask_restful import Resource, reqparse

from models.usuario import UserModel


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left empty")
        atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left empty")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The {dados['login']} already exists"}

        user = UserModel(**dados)
        user.save_user()
        return {'message': "User created successfully"}, 201
