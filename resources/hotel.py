from flask_restful import Resource

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
        return {'hoteis': hoteis}


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'Hotel not found.'}, 404 #not found ou não encontrado

    def post(self, hotel_id):
        pass

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass
