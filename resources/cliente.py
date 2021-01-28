import myconnutils
from flask_restful import Resource, reqparse


class Cliente(Resource):
    def get(self, cedula):
        cliente = self.find_by_cedula(cedula)
        if cliente:
            return cliente
        return {'message': 'Cliente no encontrado'}, 404

    @classmethod
    def find_by_cedula(cls, token):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        # query = 'SELECT `tid`,`participant_id`,`firstname`,`lastname`,`email`,`token`,`usesleft` from
        # `lime_tokens_782729` WHERE `token`= %s '
        query = '''SELECT
                    `id`,
                    `correo`,
                    `nombre`,
                    `apellidos`,
                    `cedula`,
                    `telefono`
                    FROM `cliente`
                    WHERE `cedula` = %s'''
        cursor.execute(query, (token,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return {'cliente': {
                'id': row['id'], 'correo': row['correo'],
                'nombre': row['nombre'], 'apellidos': row['apellidos'],
                'cedula': row['cedula'], 'telefono': row['telefono']
            }}

    @classmethod
    def insert(cls, usuario):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = ''
        cursor.execute(query, (usuario['firstname'],
                               usuario['lastname'],
                               usuario['email'],
                               usuario['token']
                               ))

        connection.commit()
        connection.close()


class ClientesList(Resource):
    def get(self):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = 'SELECT * FROM `cliente`'

        cursor.execute(query)

        clientes = []

        for row in cursor:
            clientes.append(
                            {
                            'id': row['id'],
                            'correo': row['correo'],
                            'nombre': row['nombre'],
                            'apellidos': row['apellidos'],
                            'cedula': row['cedula'],
                            'telefono': row['telefono']
                            }
                        )

        connection.close()
        return {'clientes': clientes}