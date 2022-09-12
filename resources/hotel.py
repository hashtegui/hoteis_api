import sqlite3

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, request

from models.hotel import HotelModel

# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400


class Hoteis(Resource):

    def normalize_path_params(cidade=None,
                              estrelas_min=0,
                              estrelas_max=5,
                              diaria_min=0,
                              diaria_max=10000,
                              limit=50,
                              offset=0, **dados):
        if cidade:
            return {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'cidade': cidade,
                'limit': limit,
                'offset': offset
            }
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        hoteis = [hotel.json() for hotel in HotelModel.query.all()]
        print('connection')
        dados_validos = request.args
        parametros = Hoteis.normalize_path_params(**dados_validos)

        if parametros.get('cidade'):
            consulta = f"""SELECT * FROM hoteis
            where (estrelas >= ? and estrelas <= ?) and
            (diaria >= ? and diaria <= ?) and cidade = ? LIMIT ? OFFSET ?"""
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = f"""SELECT * FROM hoteis
                        where (estrelas > ? and estrelas < ?) and
                        (diaria >= ? and diaria <= ?)
                         LIMIT ? OFFSET ?"""
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })

        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="The field 'nome' cannot be empty")
    argumentos.add_argument('estrelas', type=float, required=True,
                            help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        # not found ou não encontrado
        return {'message': 'Hotel not found.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            # bad request
            return {'message': f'Hotel id {hotel_id} already exists.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        # novo_hotel = {'hotel_id': hotel_id, **dados}
        try:
            hotel.save_hotel()
        except:
            # internal server error
            return {'message': 'An internal error occurred trying to save hotel'}, 500
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            # internal server error
            return {'message': 'An internal error occurred trying to save hotel'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                # internal server error
                return {'message': 'An internal error occurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
