from flask import Flask
from flask_restful import Api

from resources.cliente_natural import ClienteNaturalResource, ClientesNaturalesListResource
from resources.cliente_natural import ClienteNaturaleStepperResource, ClientesNaturalesListDesactivados
from resources.contactos_ce import ContactosListCEResource, ContactoCEResource
from resources.filtracion import FiltracionResource, FiltracionListResource
from resources.accesorio import AccesorioResource, AccesoriosListResource
from resources.ficha_tecnica import FichaTecnicaResource
from resources.oficinas_ce import OficinasCEResource, OficinasListCEResource
from resources.parroquia import ParroquiasListResource
from resources.provincia import ProvinciasListResource
from resources.canton import CantonesListResource
from resources.cliente_empresarial import MasterDetailCEResource, ClienteEmpresarialList
from resources.tipo_cargo import TipoCargoResource, TiposCargosListResource
from resources.cargo import CargoResource, CargosListResource
from resources.direccion_cliente import DireccionClienteResource, DireccionClienteListResource
from resources.VistaInfoClienteEmpresarial import VistaInfoClienteEmpresarialResource


from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config[
    'CORS_HEADERS'] = 'Content-Type'  # Le decimos a cors en que formato va a recibir los headers (datos de las peticiones)
api = Api(app)
CORS(app)
cors = CORS(app, resources={
    r"*": {"origins": ["http://app.sistagua.ec", "http://localhost:4200", "http://localhost:8000", "http://sistagua.ec",
                       "http://sistagua.ec/app"]}})  # Permitimos el origen de nuestro servidor local de frontend

api.add_resource(ClienteNaturalResource, '/cliente_natural')
api.add_resource(ClientesNaturalesListResource, '/clientes_naturales')
api.add_resource(ClienteNaturaleStepperResource, '/cliente_natural_stepper')
api.add_resource(ClientesNaturalesListDesactivados, '/clientes_naturales_desactivado')
api.add_resource(FiltracionResource, '/filtracion')
api.add_resource(FiltracionListResource, '/filtraciones')
api.add_resource(AccesorioResource, '/accesorio')
api.add_resource(AccesoriosListResource, '/accesorios')
api.add_resource(FichaTecnicaResource, '/ficha_tecnica')
api.add_resource(ParroquiasListResource, '/parroquias')
api.add_resource(ProvinciasListResource, '/provincias')
api.add_resource(CantonesListResource, '/cantones')
api.add_resource(DireccionClienteListResource, '/direcciones_cliente')
api.add_resource(TiposCargosListResource, '/tipos-cargos')
api.add_resource(TipoCargoResource, '/tipo-cargo')
api.add_resource(CargosListResource, '/cargos')
api.add_resource(CargoResource, '/cargo')
api.add_resource(MasterDetailCEResource, '/master-detail-ce')
api.add_resource(ClienteEmpresarialList, '/clientes_empresariales')
api.add_resource(VistaInfoClienteEmpresarialResource, '/info_clientes_empresariales')
api.add_resource(OficinasCEResource, '/oficina-ce')
api.add_resource(OficinasListCEResource, '/oficinas-ce/<int:fk_cliente>')
api.add_resource(ContactosListCEResource, '/cargos-ce/<int:fk_cliente>')
api.add_resource(ContactoCEResource, '/cargo-ce')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
