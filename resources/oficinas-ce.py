from http import HTTPStatus
from models.oficinas_empresa import OficinasEmpresa

import myconnutils
from flask_restful import Resource, reqparse
from flask import request

class OficinasCEResource(Resource):
    def post(self):
        data = request.get_json()

        obj_x_id = self.buscar_x_id(data['id'])

        if obj_x_id:
            return {'mensaje': 'La Oficina con este id ya existe'}, HTTPStatus.BAD_REQUEST

        oficina_id = self.guardar(data)
        if oficina_id:
            oficina_object = self.buscar_x_id(oficina_id)
            return {'oficina_ce': oficina_object}, HTTPStatus.CREATED
    
    
    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                        INSERT INTO accesorios (codigo, nombre, descripcion)
                        VALUES (%s,%s,%s)
                        """
        cursor.execute(query_insert, ((valor['codigo']).strip(), (valor['nombre']).strip(), valor['descripcion']))
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted
    
    
    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                SELECT
                    *
                    FROM oficinas_empresa
                    WHERE oficinas_empresa.fk_cliente_empresarial = %s
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            oficinas_ce = OficinasEmpresa(
                row['id'],
                row['codigo'],
                row['nombre'],
                row['descripcion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return oficinas_ce.data
        else:
            return None
