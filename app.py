from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sql_alchemy import banco

from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.site import Site, Sites
from resources.usuario import User, UserRegister, UserLogin, UserLogout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'NaofalePraNInguem'
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt = JWTManager(app)
banco.init_app(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, token: dict):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, token):
    return jsonify({'message': 'You habe been logged out'}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(Sites, '/sites')

