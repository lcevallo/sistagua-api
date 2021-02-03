import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request
from models.ficha_tecnica import FichaTecnica

class FichaTecnicaResource(Resource):
    
    
    
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