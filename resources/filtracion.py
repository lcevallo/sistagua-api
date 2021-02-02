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

    # def get(self):
    #     filtracion_filter = request.args.get('filtracion')
    #     filtracion_response = self.buscar_x_filtracion(filtracion_filter)
    #     if filtracion_response:
    #         return {'filtracion': filtracion_response}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        filtracion_id = self.guardar(data['filtracion'])
        # filtracion_id = None

        if filtracion_id:
            filtracion_object = self.buscar_x_id(filtracion_id)
            return {'filtracion': filtracion_object}, HTTPStatus.CREATED

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = "INSERT INTO filtracion (filtracion) VALUES (%s)"
        cursor.execute(query_insert, (valor,))
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted

    @classmethod
    def buscar_x_filtracion(cls,filter):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where filtracion = %s AND publish=true"
        cursor.execute(query, (filter,))
        row = cursor.fetchone()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['filtracion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )

        connection.close()
        return filtracion.data

    @classmethod
    def buscar_x_id(cls,id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from sistagua_bd.filtracion where id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row:
            filtracion = Filtracion(
                row['id'],
                row['filtracion'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )

        connection.close()
        return filtracion.data
