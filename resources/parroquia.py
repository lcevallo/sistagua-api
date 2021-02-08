from http import HTTPStatus
from models.parroquia import Parroquia

import myconnutils
from flask_restful import Resource, reqparse
from flask import request


class ParroquiasListResource(Resource):
    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            parroquias_list = self.buscar()
        else:
            str1 = " "
            for key in keys:
                if key == 'id_canton':
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                else:
                    column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            parroquias_list = self.buscar_x_criterio(str1.join(column_where))

        return {'parroquias': parroquias_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_parroquia where 1=1 {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                parroquia = Parroquia(
                    row['id'],
                    row['parroquia'],
                    row['id_canton']
                )
                data.append(parroquia.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_parroquia "
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                parroquia = Parroquia(
                    row['id'],
                    row['parroquia'],
                    row['id_canton']
                )
                data.append(parroquia.data)

        return data
