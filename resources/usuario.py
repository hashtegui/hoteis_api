from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left empty")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left empty")
atributos.add_argument('ativado', type=bool)


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The {dados['login']} already exists"}

        user = UserModel(**dados)
        user.ativado = False
        user.save_user()
        return {'message': "User created successfully"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and user.senha == dados['senha']:
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'acess_token': token_de_acesso}
            return {'message': 'User not confirmed'}, 400
        return {'message': 'The username or password is incorrect'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Indentifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200
    
class UserConfirm(Resource):
    #raiz do site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
        
        if not user:
            return {"message": f'User id {user_id} not found'}, 404
        
        user.ativado = True
        user.save_user()
        
        return {'message': f'User id {user_id} confirmed successfully'}