from http import HTTPStatus

import myconnutils
from flask_restful import Resource
from flask import request

from models.cargo import Cargo


class CargoResource(Resource):
    def post(self):
        data = request.get_json()
        cargo_id = self.guardar(data)
        if cargo_id:
            cargo_object = self.buscar_x_id(cargo_id)
            return {'cargo': cargo_object}, HTTPStatus.CREATED

    def delete(self):
        id = request.args.get('id')
        cargo_response = self.buscar_x_id(id)
        if cargo_response:
            cantidad = self.eliminar(id)
            return {}, HTTPStatus.NO_CONTENT
        else:
            return {'message': 'cargo con id no encontrado en la base'}, HTTPStatus.NOT_FOUND

    def put(self):
        data = request.get_json()
        # id = request.args.get('id')
        # id = data['id']
        cargo_respuesta = self.actualizar(data)
        cargo_response = self.buscar_x_id(data['id'])
        if cargo_response:
            return {'cargo': cargo_response}, HTTPStatus.OK

    @classmethod
    def guardar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                            INSERT INTO cargo (fk_tipo_cargo, nombres, apellidos, celular, correo)
                            VALUES (%s, %s, %s, %s, %s)
                        """
        cursor.execute(query_insert, (valor['fk_tipo_cargo'], valor['nombres'], valor['apellidos'], valor['celular'], valor['correo']))
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted

    @classmethod
    def eliminar(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """
                        UPDATE cargo
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
                        UPDATE cargo
                        SET fk_tipo_cargo = %s,
                            nombres = %s,
                            apellidos = %s,
                            celular = %s,
                            correo = %s
                        WHERE id = %s
                        AND publish = true
                        """
        cursor.execute(query_update, (valor['fk_tipo_cargo'], valor['nombres'], valor['apellidos'], valor['celular'], valor['correo'], valor['id']))
        connection.commit()

        respuesta = cursor.rowcount

        print(cursor.rowcount, "record(s) affected logic deleted!")
        connection.close()
        return respuesta

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                SELECT
                cargo.*
                FROM cargo
                WHERE cargo.id = %s AND publish = true
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cargo = Cargo(
                row['id'],
                row['fk_tipo_cargo'],
                row['nombres'],
                row['apellidos'],
                row['celular'],
                row['correo'],
                row['publish']
            )
            return cargo.data
        else:
            return None


class CargosListResource(Resource):
    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            cargos_list = self.buscar()
        else:
            # cedula = request.args.get('cedula')
            numeros = ['id', 'fk_tipo_cargo']
            varchars = ['nombres', 'apellidos', 'celular', 'correo']
            str1 = " "
            for key in keys:
                if key in numeros:
                    column_where.append((" AND " + str(key) + " = {} ").format(request.args.get(key)))
                elif key in varchars:
                    column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            cargos_list = self.buscar_x_criterio(str1.join(column_where))

        return {'cargos': cargos_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  * FROM cargo WHERE publish=true {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                cargo = Cargo(
                    row['id'],
                    row['fk_tipo_cargo'],
                    row['nombres'],
                    row['apellidos'],
                    row['celular'],
                    row['correo'],
                    row['publish']
                )
                data.append(cargo.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  * FROM cargo where publish=true "
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                cargo = Cargo(
                    row['id'],
                    row['fk_tipo_cargo'],
                    row['nombres'],
                    row['apellidos'],
                    row['celular'],
                    row['correo'],
                    row['publish']
                )
                data.append(cargo.data)
        return data
