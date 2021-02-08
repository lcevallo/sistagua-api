from http import HTTPStatus
from models.provincia import Provincia

import myconnutils
from flask_restful import Resource, reqparse
from flask import request


class ProvinciasListResource(Resource):
    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            provincias_list = self.buscar()
        else:
            str1 = " "
            for key in keys:
                if key == 'id':
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                else:
                    column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            provincias_list = self.buscar_x_criterio(str1.join(column_where))

        return {'provincias': provincias_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_provincia where 1=1 {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                provincia = Provincia(
                    row['id'],
                    row['provincia']
                )
                data.append(provincia.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_provincia "
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                provincia = Provincia(
                    row['id'],
                    row['provincia']
                )
                data.append(provincia.data)

        return data
