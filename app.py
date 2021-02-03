from flask import Flask
from flask_restful import Api

from resources.cliente import Cliente, ClientesList
from resources.filtracion import FiltracionResource
from resources.accesorio import AccesorioResource, AccesoriosListResource

app = Flask(__name__)
api = Api(app)

api.add_resource(Cliente, '/cliente/<string:cedula>')
api.add_resource(ClientesList, '/clientes')
api.add_resource(FiltracionResource, '/filtracion')
api.add_resource(AccesorioResource, '/accesorio')
api.add_resource(AccesoriosListResource, '/accesorios')

if __name__ == '__main__':
    app.run(port=5000, debug=True)