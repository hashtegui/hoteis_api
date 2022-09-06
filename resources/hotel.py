from flask_restful import Resource, reqparse

from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alha hotel',
        'estrelas': 4.5,
        'diaria': 300.90,
        'cidade': 'Manaus'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo hotel',
        'estrelas': 4.8,
        'diaria': 312.90,
        'cidade': 'Manaus'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie hotel',
        'estrelas': 4.98,
        'diaria': 400.00,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'omega',
        'nome': 'Omega hotel',
        'estrelas': 4.1,
        'diaria': 350.00,
        'cidade': 'Manaus'
    },
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  # not found ou não encontrado

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already exists.'}, 400  # bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        # novo_hotel = {'hotel_id': hotel_id, **dados}

        hotel.save_hotel()
        return hotel.json(), 201

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
