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
                        INSERT INTO oficinas_empresa (fk_cliente_empresarial, fk_provincia, fk_canton, fk_parroquia, sector, direccion, telefono_convencional)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
        cursor.execute(query_insert, (
            valor['fkClienteEmpresa'],
            valor['fkProvincia'],
            valor['fkCanton'],
            valor['fkParroquia'],
            (valor['sector']).strip(),
            (valor['direccion']).strip(),
            (valor['telefono_convencional']).strip()
        )
                       )
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
                    WHERE oficinas_empresa.id = %s
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            oficinas_ce = OficinasEmpresa(
                row['id'],
                row['fk_cliente_empresarial'],
                row['fk_provincia'],
                row['fk_canton'],
                row['fk_parroquia'],
                row['sector'],
                row['direccion'],
                row['telefono_convencional'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return oficinas_ce.data
        else:
            return None


class OficinasListCEResource(Resource):
    def get(self, fk_cliente):
        oficinas_list = self.find_all_by_cliente(fk_cliente)

        if oficinas_list is None:
            return {'mensaje': 'No existen oficinas para este cliente empresarial'}, HTTPStatus.NOT_FOUND

        return {'oficinas': oficinas_list}

    @classmethod
    def find_all_by_cliente(cls, fk_cliente):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query = '''
                SELECT
                  *
                FROM oficinas_empresa
                WHERE oficinas_empresa.fk_cliente_empresarial = %s
                '''

        cursor.execute(query, (fk_cliente,))
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                oficinas_ce = OficinasEmpresa(
                    row['id'],
                    row['fk_cliente_empresarial'],
                    row['fk_provincia'],
                    row['fk_canton'],
                    row['fk_parroquia'],
                    row['sector'],
                    row['direccion'],
                    row['telefono_convencional'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(oficinas_ce.data)

        return data





