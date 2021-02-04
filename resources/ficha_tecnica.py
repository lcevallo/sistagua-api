import myconnutils
import datetime
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request
from models.ficha_tecnica import FichaTecnica


class FichaTecnicaResource(Resource):
    def get(self):
        id = request.args.get('id')
        ficha_tecnica = self.buscar_x_id(id)
        if ficha_tecnica:
            return ficha_tecnica
        return {'message': 'Cliente no encontrado'}, 404

    def post(self):
        data = request.get_json()

        ficha_tecnica_object = self.find_by_cedula(data['cedula'])
        if ficha_tecnica_object is not None:
            return {'mensaje': 'la ficha tecnica para ese usuario ya existe en la base de datos'}
        else:
            ficha_tecnica_id = self.insert(data)
            if ficha_tecnica_id:
                ficha_tecnica_object = self.buscar_x_id(ficha_tecnica_id)
                print(ficha_tecnica_object)
                return {'ficha_tecnica': ficha_tecnica_object}, HTTPStatus.CREATED

    @classmethod
    def find_by_cedula(cls, cedula):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        # query = 'SELECT `tid`,`participant_id`,`firstname`,`lastname`,`email`,`token`,`usesleft` from
        # `lime_tokens_782729` WHERE `token`= %s '
        query = '''
                    SELECT
                    ficha_tecnica.*
                    FROM ficha_tecnica
                    INNER JOIN cliente_ficha
                        ON ficha_tecnica.fk_cliente = cliente_ficha.id
                    WHERE cliente_ficha.cedula = %s
                    AND ficha_tecnica.publish = TRUE
                '''
        cursor.execute(query, (cedula,))
        row = cursor.fetchone()
        connection.close()

        if row:
            ficha_tecnica = FichaTecnica(
                row['id'],
                row['fk_cliente'],
                row['tds'],
                row['ppm'],
                row['visitas'],
                row['fecha_comprado'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return ficha_tecnica.data
        else:
            return None

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                SELECT
                ficha_tecnica.*
                FROM ficha_tecnica
                WHERE ficha_tecnica.publish = TRUE
                AND ficha_tecnica.id = %s
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            ficha_tecnica = FichaTecnica(
                row['id'],
                row['fk_cliente'],
                row['tds'],
                row['ppm'],
                row['visitas'],
                row['fecha_comprado'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return ficha_tecnica.data
        else:
            return None

    @classmethod
    def insert(cls, valor):
        fecha_comprado_format = datetime.datetime.strptime(valor['fecha_comprado'], "%Y-%m-%d")
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query_insert = """
                       INSERT INTO
                            `ficha_tecnica`(
                            `fk_cliente`,
                            `tds`,
                            `ppm`,
                            `visitas`,
                            `fecha_comprado`)
                            VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s)
                        """
        cursor.execute(query_insert, (
            valor['fk_cliente'],
            valor['tds'],
            valor['ppm'],
            valor['visitas'],
            fecha_comprado_format
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
    def eliminar(cls, cedula):
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
