from http import HTTPStatus
from models.accesorios import Accesorio

import myconnutils
from flask_restful import Resource, reqparse
from flask import request


class AccesorioResource(Resource):

    def get(self):
        id = request.args.get('id')
        accesorio_response = self.buscar_x_id(id)
        if accesorio_response:
            return {'accesorio': accesorio_response}, HTTPStatus.OK
        else:
            return {'message': 'Cliente no encontrado'}, 404

    def post(self):
        data = request.get_json()
        accesorio_id = self.guardar(data)
        # filtracion_id = None

        if accesorio_id:
            accesorio_object = self.buscar_x_id(accesorio_id)
            return {'accesorio': accesorio_object}, HTTPStatus.CREATED

    def delete(self):
        id = request.args.get('id')
        accesorio_response = self.buscar_x_id(id)
        if accesorio_response:
            self.eliminar(id)
            return {}, HTTPStatus.NO_CONTENT
        else:
            return {'message': 'accesorio con id no encontrada en la base'}, HTTPStatus.NOT_FOUND

    def put(self):
        data = request.get_json()
        id = request.args.get('id')

        accesorio_respuesta = self.actualizar(id, data)
        # keys= [i for i in request.args.keys()]
        # keys= [i for i in request.get_json().keys()]
        # request.args.getlist()
        accesorio_response = self.buscar_x_id(id)
        if accesorio_response:
            return {'accesorio': accesorio_response}, HTTPStatus.OK

    @classmethod
    def eliminar(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """UPDATE accesorios
                        SET 
                        publish = FALSE,
                        updated_at = CURRENT_TIMESTAMP()
                        WHERE id = %s
                        """
        cursor.execute(query_update, (id,))
        connection.commit()

        print(cursor.rowcount, "record(s) affected logic deleted!")
        connection.close()

    @classmethod
    def actualizar(cls, id, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """UPDATE accesorios
                            SET nombre = %s,
                                descripcion = %s,
                                updated_at = CURRENT_TIMESTAMP()
                            WHERE id = %s
                        """
        cursor.execute(query_update, (valor['nombre'],
                                      valor['descripcion']
                                      , id))
        connection.commit()

        print(cursor.rowcount, "record(s) affected")
        connection.close()

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                        INSERT INTO accesorios (nombre, descripcion, created_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP())
                        """
        cursor.execute(query_insert, (valor['nombre'], valor['descripcion']))
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
                accesorios.*
                FROM accesorios
                WHERE accesorios.id = %s
                AND publish=true
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            accesorio = Accesorio(
                row['id'],
                row['nombre'],
                row['descripcion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return accesorio.data
        else:
            return None

    @classmethod
    def buscar_x_filtracion(cls, filter):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where filtracion = %s AND publish=true"
        cursor.execute(query, (filter,))
        row = cursor.fetchone()
        connection.close()

        if row:
            accesorio = Accesorio(
                row['id'],
                row['nombre'],
                row['descripcion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return accesorio.data
        else:
            return None


class AccesoriosListResource(Resource):

    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            accesorios_list = self.buscar()
        else:
            str1 = " "
            for key in keys:
                column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))
            accesorios_list = self.buscar_x_criterio(str1.join(column_where))

        return {'accesorios': accesorios_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from accesorios where publish=true {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                accesorio = Accesorio(
                    row['id'],
                    row['nombre'],
                    row['descripcion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(accesorio.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from accesorios where publish=true"
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                accesorios = Accesorio(
                    row['id'],
                    row['nombre'],
                    row['descripcion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(accesorios.data)

        return data
