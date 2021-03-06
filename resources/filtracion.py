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

        obj_x_codigo = self.buscar_x_codigo(data['codigo'])

        if obj_x_codigo:
            return {'mensaje': 'La filtracion con este codigo ya existe'}, HTTPStatus.BAD_REQUEST

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
                            SET codigo = %s,
                                nombre = %s,
                                descripcion = %s,
                                updated_at = CURRENT_TIMESTAMP()
                            WHERE id = %s
                        """
        cursor.execute(query_update, (valor['codigo'], valor['nombre'], valor['descripcion'], id))
        connection.commit()

        print(cursor.rowcount, "record(s) affected")
        connection.close()

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = "INSERT INTO filtracion (codigo,nombre,descripcion) VALUES (%s,%s,%s)"
        cursor.execute(query_insert, (valor['codigo'], valor['nombre'], valor['descripcion']))
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted

    @classmethod
    def buscar_x_filtracion(cls, filter):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where nombre = %s AND publish=true"
        cursor.execute(query, (filter,))
        row = cursor.fetchone()
        connection.close()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['codigo'],
                row['nombre'],
                row['descripcion'],
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
                row['codigo'],
                row['nombre'],
                row['descripcion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return filtracion.data
        else:
            return None

    @classmethod
    def buscar_x_codigo(cls, codigo):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where codigo = %s AND publish=true"
        cursor.execute(query, (codigo,))
        row = cursor.fetchone()
        connection.close()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['codigo'],
                row['nombre'],
                row['descripcion'],
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

        query = "SELECT * from filtracion where publish=true {} ORDER BY nombre ASC".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                filtracion = Filtracion(
                    row['id'],
                    row['codigo'],
                    row['nombre'],
                    row['descripcion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(filtracion.data)

        connection.close()
        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from filtracion where publish=true ORDER BY nombre ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print(rows)

        data = []

        for row in rows:
            if row:
                filtracion = Filtracion(
                    row['id'],
                    row['codigo'],
                    row['nombre'],
                    row['descripcion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(filtracion.data)

        connection.close()
        return data