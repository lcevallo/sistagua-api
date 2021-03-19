import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request, json
from models.vista_info_cliente_empresarial import VistaInfoClienteEmpresarial


class VistaInfoClienteEmpresarialResource(Resource):
    def get(self):
        id = request.args.get('id')
        # id = data['id']
        cliente_empresarial = self.buscar_x_id(id)

        if not cliente_empresarial:
            return {'mensaje': f'Cliente con id {id} no existe en la base de datos.'}

        return {'cliente_empresarial': cliente_empresarial}, HTTPStatus.OK

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from v_info_cliente_empresarial where id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cliente_empresarial = VistaInfoClienteEmpresarial(
                row['id'],
                row['codigo'],
                row['ruc'],
                row['nombre_empresa'],
                row['direccion'],
                row['telefono'],
                row['correo_empresa'],
                row['nombres'],
                row['apellidos'],
                row['tipo'],
                row['celular'],
                row['cumple'],
                row['correo_cargo'],
                row['provincia'],
                row['canton'],
                row['parroquia'],
                row['sector'],
                row['direccion_cargo'],
                row['telefono_convencional'],
                row['publish']
            )
            return cliente_empresarial.data
        else:
            return None
