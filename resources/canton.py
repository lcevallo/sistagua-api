from http import HTTPStatus
from models.canton import Canton

import myconnutils
from flask_restful import Resource, reqparse
from flask import request


class CantonesListResource(Resource):
    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            cantones_list = self.buscar()
        else:
            str1 = " "
            for key in keys:
                if key == 'id':
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                elif key == 'id_provincia':
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                else:
                    column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            cantones_list = self.buscar_x_criterio(str1.join(column_where))

        return {'cantones': cantones_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_canton where 1=1 {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                canton = Canton(
                    row['id'],
                    row['canton'],
                    row['id_provincia']
                )
                data.append(canton.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from tbl_canton "
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                canton = Canton(
                    row['id'],
                    row['canton'],
                    row['id_provincia']
                )
                data.append(canton.data)

        return data
