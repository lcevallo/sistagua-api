from http import HTTPStatus

import myconnutils
from flask_restful import Resource
from flask import request

from models.tipo_cargo import TipoCargo


class TipoCargoResource(Resource):
    def post(self):
        data = request.get_json()

        tipo_cargo_object = self.get_x_tipo(data['tipo'])

        if tipo_cargo_object is not None:
            return {'mensaje': 'El tipo de cargo ya existe en la base de datos'}, HTTPStatus.BAD_REQUEST
        else:
            tipo_cargo_id = self.guardar(data)
            if tipo_cargo_id:
                tipo_cargo_object = self.buscar_x_id(tipo_cargo_id)
                return {'tipo_cargo': tipo_cargo_object}, HTTPStatus.CREATED

    def put(self):
        data = request.get_json()
        id = data['id']
        cantidad = self.actualizar(data)

        tipo_cargo_respuesta = self.buscar_x_id(data['id'])
        if tipo_cargo_respuesta:
            return {'tipo-cargo': tipo_cargo_respuesta}, HTTPStatus.OK

    def delete(self):
        id = request.args.get('id')
        tipo_cargo_response = self.buscar_x_id(id)
        if tipo_cargo_response:
            cantidad = self.eliminar(id)
            return {}, HTTPStatus.NO_CONTENT
        else:
            return {'message': 'tipo cargo con id no encontrado en la base'}, HTTPStatus.NOT_FOUND

    @classmethod
    def eliminar(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """
                        UPDATE tipo_cargo
                        SET publish = FALSE
                        WHERE id = %s
                        """
        cursor.execute(query_update, (id,))
        connection.commit()

        respuesta = cursor.rowcount

        print(cursor.rowcount, "record(s) affected logic deleted!")
        connection.close()
        return respuesta

    @classmethod
    def actualizar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """
                        UPDATE tipo_cargo
                        SET tipo = %s
                        WHERE id = %s AND publish= true
                        """
        cursor.execute(query_update, (valor['tipo'], valor['id']))
        connection.commit()

        respuesta = cursor.rowcount

        print(cursor.rowcount, "record(s) affected logic deleted!")
        connection.close()
        return respuesta

    @classmethod
    def get_x_tipo(cls, tipo):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                        SELECT
                        tipo_cargo.*
                        FROM tipo_cargo
                        WHERE tipo_cargo.tipo = %s
                        AND publish = true
                        """
        cursor.execute(query, (tipo,))
        row = cursor.fetchone()
        connection.close()

        if row:
            tipo_cargo = TipoCargo(
                row['id'],
                row['tipo'],
                row['publish']
            )
            return tipo_cargo.data
        else:
            return None

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                    INSERT INTO tipo_cargo(
                                tipo)
                                VALUES(
                                %s)
                        """
        cursor.execute(query_insert, (valor['tipo'],))
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
                tipo_cargo.*
                FROM tipo_cargo
                WHERE tipo_cargo.id = %s
                AND publish=true
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            tipo_cargo = TipoCargo(
                row['id'],
                row['tipo'],
                row['publish']
            )
            return tipo_cargo.data
        else:
            return None


class TiposCargosListResource(Resource):
    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            tipos_cargos_list = self.buscar()
        else:
            # cedula = request.args.get('cedula')
            numeros = ['id']
            varchars = ['tipo']
            str1 = " "
            for key in keys:
                if key in numeros:
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                elif key in varchars:
                    column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            tipos_cargos_list = self.buscar_x_criterio(str1.join(column_where))

        return {'tipos_cargos': tipos_cargos_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  tipo_cargo.* FROM tipo_cargo WHERE publish=true {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                tipo_cargo = TipoCargo(
                    row['id'],
                    row['tipo'],
                    row['publish']

                )
                data.append(tipo_cargo.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  * FROM tipo_cargo WHERE publish=true"
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                tipo_cargo = TipoCargo(
                    row['id'],
                    row['tipo'],
                    row['publish']
                )
                data.append(tipo_cargo.data)
        return data
