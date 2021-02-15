from flask import Flask
from flask_restful import Api

from resources.cliente_natural import ClienteNaturalResource, ClientesNaturalesListResource
from resources.filtracion import FiltracionResource,FiltracionListResource
from resources.accesorio import AccesorioResource, AccesoriosListResource
from resources.ficha_tecnica import FichaTecnicaResource
from resources.parroquia import ParroquiasListResource
from resources.provincia import ProvinciasListResource
from resources.canton import CantonesListResource
from flask_cors import CORS, cross_origin


UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS= {"png", "jpg","jpeg","gif"}


def allowed_files(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['CORS_HEADERS']= 'Content-Type'  #Le decimos a cors en que formato va a recibir los headers (datos de las peticiones)
api = Api(app)
CORS(app)
cors = CORS(app,resources = {r"*": {"origins": "http://localhost:4200"}}) #Permitimos el origen de nuestro servidor local de frontend

api.add_resource(ClienteNaturalResource, '/cliente_natural')
api.add_resource(ClientesNaturalesListResource, '/clientes_naturales')
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