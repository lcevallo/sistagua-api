from http import HTTPStatus
from models.filtracion import Filtracion

import myconnutils
from flask_restful import Resource, reqparse
from flask import request


class FiltracionResource(Resource):

    def get(self):
        id = request.args.get('id')
        filtracion_response = self.buscar_x_id(id)
        if filtracion_response:
            return {'filtracion': filtracion_response}, HTTPStatus.OK
        else:
            return {'message': 'Filtracion no encontrado'}, 404

    # def get(self):
    #     filtracion_filter = request.args.get('filtracion')
    #     filtracion_response = self.buscar_x_filtracion(filtracion_filter)
    #     if filtracion_response:
    #         return {'filtracion': filtracion_response}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        filtracion_id = self.guardar(data)
        if filtracion_id:
            filtracion_object = self.buscar_x_id(filtracion_id)
            return {'filtracion': filtracion_object}, HTTPStatus.CREATED

    def delete(self):
        id = request.args.get('id')
        filtracion_response = self.buscar_x_id(id)
        if filtracion_response:
            self.eliminar(id)
            return {}, HTTPStatus.NO_CONTENT
        else:
            return {'message': 'filtracion con id no encontrada en la base'}, HTTPStatus.NOT_FOUND

    def put(self):
        data = request.get_json()
        id = request.args.get('id')
        filtracion_respuesta = self.actualizar(id, data)
        filtracion_response = self.buscar_x_id(id)
        if filtracion_response:
            return {'filtracion': filtracion_response}, HTTPStatus.OK

    @classmethod
    def eliminar(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """UPDATE filtracion
                            SET publish = false,
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
        query_update = """UPDATE filtracion
                            SET filtracion = %s,
                                updated_at = CURRENT_TIMESTAMP()
                            WHERE id = %s
                        """
        cursor.execute(query_update, (valor['filtracion'], id))
        connection.commit()

        print(cursor.rowcount, "record(s) affected")
        connection.close()

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = "INSERT INTO filtracion (filtracion) VALUES (%s)"
        cursor.execute(query_insert, (valor['filtracion'],))
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted

    @classmethod
    def buscar_x_filtracion(cls, filter):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where filtracion = %s AND publish=true"
        cursor.execute(query, (filter,))
        row = cursor.fetchone()
        connection.close()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['filtracion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return filtracion.data
        else:
            return None

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where id = %s AND publish=true"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['filtracion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return filtracion.data
        else:
            return None


class FiltracionListResource(Resource):

    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            filtraciones_list = self.buscar()
        else:
            str1 = " "
            for key in keys:
                column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))
            filtraciones_list = self.buscar_x_criterio(str1.join(column_where))

        return {'filtraciones': filtraciones_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from filtracion where publish=true {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                accesorio = Filtracion(
                    row['id'],
                    row['filtracion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(accesorio.data)

        connection.close()
        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from filtracion where publish=true"
        cursor.execute(query, (id,))
        rows = cursor.fetchAll()

        data = []

        for row in rows:
            if row:
                accesorios = Filtracion(
                    row['id'],
                    row['filtracion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(accesorios.data)

        connection.close()
        return data
