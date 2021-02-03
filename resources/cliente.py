import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request
from models.cliente import Cliente


class ClienteResource(Resource):
    def get(self):
        cedula = request.args.get('cedula')
        cliente = self.find_by_cedula(cedula)
        if cliente:
            return cliente
        return {'message': 'Cliente no encontrado'}, 404

    def post(self):
        data = request.get_json()

        cliente_object = self.find_by_cedula(data['cedula'])
        if cliente_object is not None:
            return {'mensaje': 'El cliente ya existe en la base de datos'}
        else:
            cliente_id = self.insert(data)
            if cliente_id:
                cliente_object = self.buscar_x_id(cliente_id)
                print(cliente_object)
                return {'cliente': cliente_object}, HTTPStatus.CREATED

    def put(self):
        data = request.get_json()
        id = request.args.get('id')

        cliente_respuesta = self.actualizar(id, data)
        # keys= [i for i in request.args.keys()]
        # keys= [i for i in request.get_json().keys()]
        # request.args.getlist()
        cliente_response = self.buscar_x_id(id)
        if cliente_response:
            return {'cliente': cliente_response}, HTTPStatus.OK

    def delete(self):
        cedula = request.args.get('cedula')
        cliente_response = self.find_by_cedula(cedula)
        if cliente_response:
            self.eliminar(cedula)
            return {}, HTTPStatus.NO_CONTENT
        else:
            return {'message': 'filtracion con id no encontrada en la base'}, HTTPStatus.NOT_FOUND

    @classmethod
    def find_by_cedula(cls, cedula):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        # query = 'SELECT `tid`,`participant_id`,`firstname`,`lastname`,`email`,`token`,`usesleft` from
        # `lime_tokens_782729` WHERE `token`= %s '
        query = '''
                    SELECT
                    cliente_ficha.*
                    FROM cliente_ficha                  
                    WHERE cedula = %s AND publish= true
                '''
        cursor.execute(query, (cedula,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cliente = Cliente(
                row['id'],
                row['correo'],
                row['nombre'],
                row['apellidos'],
                row['cedula'],
                row['telefono'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return cliente.data
        else:
            return None

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                SELECT
                *
                FROM cliente_ficha
                WHERE id = %s AND publish= true
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cliente = Cliente(
                row['id'],
                row['correo'],
                row['nombre'],
                row['apellidos'],
                row['cedula'],
                row['telefono'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return cliente.data
        else:
            return None

    @classmethod
    def insert(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                        INSERT INTO cliente_ficha (correo, nombre, apellidos, cedula, telefono, created_at)
                        VALUES ( %s ,  %s ,  %s ,  %s ,  %s , CURRENT_TIMESTAMP())
                        """
        cursor.execute(query_insert, (
            valor['correo'],
            valor['nombre'],
            valor['apellidos'],
            valor['cedula'],
            valor['telefono']
        )
                       )
        connection.commit()
        id_inserted = cursor.lastrowid
        connection.close()
        return id_inserted

    @classmethod
    def actualizar(cls, id, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """
                        UPDATE cliente_ficha
                        SET correo = %s,
                            nombre = %s,
                            apellidos = %s,
                            cedula = %s,
                            telefono = %s,
                            updated_at = CURRENT_TIMESTAMP()
                        WHERE
                        id = %s AND
                        publish = true
                        """
        cursor.execute(query_update, (
            valor['correo'],
            valor['nombre'],
            valor['apellidos'],
            valor['cedula'],
            valor['telefono']
            , id))
        connection.commit()

        print(cursor.rowcount, "record(s) affected")
        connection.close()

    @classmethod
    def eliminar(cls,cedula):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_update = """UPDATE cliente_ficha
                            SET publish = false,
                                updated_at = CURTIME()
                            WHERE cedula = %s
                        """
        cursor.execute(query_update, (cedula,))
        connection.commit()

        print(cursor.rowcount, "record(s) affected logic deleted!")
        connection.close()


class ClientesListResource(Resource):

    def get(self):
        column_where = []
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            clientes_list = self.buscar()
        else:
            str1 = " "
            # for i in range(len(keys)):
            #     if i == 0:
            #         column_where.append((" " + str(keys[i]) + " like '%{}%' ").format(request.args.get(keys[i])))
            #     else:
            #         column_where.append((" AND " + str(keys[i]) + " like '%{}%' ").format(request.args.get(keys[i])))

            for key in keys:
                column_where.append((" AND " + str(key) + " like '%{}%' ").format(request.args.get(key)))

            clientes_list = self.buscar_x_criterio(str1.join(column_where))

        return {'clientes': clientes_list}, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from cliente_ficha where publish = true {}".format(criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                cliente = Cliente(
                    row['id'],
                    row['correo'],
                    row['nombre'],
                    row['apellidos'],
                    row['cedula'],
                    row['telefono'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(cliente.data)

        connection.close()
        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from cliente_ficha where publish=true"

        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                cliente = Cliente(
                    row['id'],
                    row['correo'],
                    row['nombre'],
                    row['apellidos'],
                    row['cedula'],
                    row['telefono'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(cliente.data)

        connection.close()
        return data