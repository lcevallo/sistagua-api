from flask import Flask
from flask_restful import Api

from resources.cliente import ClienteResource, ClientesListResource
from resources.filtracion import FiltracionResource,FiltracionListResource
from resources.accesorio import AccesorioResource, AccesoriosListResource
from resources.ficha_tecnica import FichaTecnicaResource
from resources.parroquia import ParroquiasListResource
from resources.provincia import ProvinciasListResource
from resources.canton import CantonesListResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ClienteResource, '/cliente')
api.add_resource(ClientesListResource, '/clientes')
api.add_resource(FiltracionResource, '/filtracion')
api.add_resource(FiltracionListResource, '/filtraciones')
api.add_resource(AccesorioResource, '/accesorio')
api.add_resource(AccesoriosListResource, '/accesorios')
api.add_resource(FichaTecnicaResource, '/ficha_tecnica')
api.add_resource(ParroquiasListResource, '/parroquias')
api.add_resource(ProvinciasListResource, '/provincias')
api.add_resource(CantonesListResource, '/cantones')

if __name__ == '__main__':
    app.run(port=5000, debug=True)