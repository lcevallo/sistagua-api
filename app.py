from flask import Flask
from flask_restful import Api

from resources.cliente import Cliente, ClientesList

app = Flask(__name__)
api = Api(app)

api.add_resource(Cliente, '/cliente/<string:cedula>')
api.add_resource(ClientesList, '/clientes')


if __name__ == '__main__':
    app.run(port=5000, debug=True)