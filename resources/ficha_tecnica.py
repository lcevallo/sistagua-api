import datetime
import re
from http import HTTPStatus

from flask import request
from flask_restful import Resource

import myconnutils
from models.ficha_tecnica import FichaTecnica


class FichaTecnicaResource(Resource):
    def get(self):
        id = request.args.get('id')
        ficha_tecnica = self.buscar_x_id(id)
        if ficha_tecnica:
            return ficha_tecnica
        return {'message': 'Ficha tecnica no encontrada'}, 404

    def post(self):
        data = request.get_json()

        ficha_tecnica_object = self.find_by_cedula(data['cedula'], data['codigo'])
        if ficha_tecnica_object is not None:
            return {'mensaje': 'la ficha tecnica para ese usuario ya existe en la base de datos'}
        else:
            ficha_tecnica_id = self.insert(data)
            if ficha_tecnica_id:
                ficha_tecnica_object = self.buscar_x_id(ficha_tecnica_id)
                print(ficha_tecnica_object)
                return {'ficha_tecnica': ficha_tecnica_object}, HTTPStatus.CREATED

    @classmethod
    def find_by_cedula(cls, cedula, codigo):
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
                    AND ficha_tecnica.codigo = %s
                    AND ficha_tecnica.publish = TRUE
                '''
        cursor.execute(query, (cedula, codigo))
        row = cursor.fetchone()
        connection.close()

        if row:
            ficha_tecnica = FichaTecnica(
                row['id'],
                row['fk_cliente'],
                row['codigo'],
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
                row['codigo'],
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
                            `codigo`,
                            `tds`,
                            `ppm`,
                            `visitas`,
                            `fecha_comprado`)
                            VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s)
                        """
        cursor.execute(query_insert, (
            valor['fk_cliente'],
            valor['codigo'],
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


class FichaTecnicaListResource(Resource):
    def post(self):
        json_data = request.get_json()
        detalle_items = json_data['detalle']
        del json_data['detalle']
        return self.guardar(json_data, detalle_items)

    @classmethod
    def guardar(cls, ficha_tecnica_json, ficha_tecnica_detalle_json):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        fecha_comprado = cls.getFechaFormateada(ficha_tecnica_json['fecha_comprado'])

        query_fecha_tecnica_insert = """
                            INSERT INTO ficha_tecnica (fk_cliente, tipo_cliente, codigo, tds, ppm, visitas, fecha_comprado)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                       """

        query_fecha_tecnica_detalle_insert = """
                                   INSERT INTO ficha_tecnica_detalle (fk_ficha_tecnica, factura, fecha_mantenimiento, recibo, ficha_tecnica, descripcion, persona_recepta, firma_url, cedula_receptor, persona_dio_mantenimiento, cedula_dio_mantenimiento)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                               """

        if ficha_tecnica_json['id'] == 0:
            cursor.execute(query_fecha_tecnica_insert, (
                ficha_tecnica_json['fk_cliente'],
                ficha_tecnica_json['tipo_cliente'],
                (ficha_tecnica_json['codigo']).strip(),
                ficha_tecnica_json['tds'],
                ficha_tecnica_json['ppm'],
                ficha_tecnica_json['visitas'],
                fecha_comprado
            )
                           )

            id_ficha_tecnica = cursor.lastrowid
            insert_ids = []
            connection.commit()

        for row in ficha_tecnica_detalle_json:
            if row:
                if row['fk_ficha_tecnica'] == 0:
                    cursor.execute(query_fecha_tecnica_detalle_insert,
                                   (
                                       id_ficha_tecnica,
                                       (row['factura']).strip(),
                                       cls.getFechaFormateada(row['fecha_mantenimiento']),
                                       (row['recibo']).strip(),
                                       (row['ficha_tecnica']).strip(),
                                       (row['descripcion']).strip(),
                                       (row['persona_recepta']).strip(),
                                       (row['firma_url']).strip(),
                                       (row['cedula_receptor']).strip(),
                                       (row['persona_dio_mantenimiento']).strip(),
                                       (row['cedula_dio_mantenimiento']).strip()
                                   )
                                   )
                    insert_ids.append(cursor.lastrowid)
        # Al final
        connection.commit()
        connection.close()
        return {'id_ficha_tecnica': id_ficha_tecnica, 'ids_detalles': insert_ids}

    @classmethod
    def getFechaFormateada(cls, fecha_no_formateada):
        if fecha_no_formateada:
            fecha_comprado = re.search('\d{4}-\d{2}-\d{2}', fecha_no_formateada)
            fecha_formateada = datetime.datetime.strptime(fecha_comprado.group(), '%Y-%m-%d').date()
        else:
            fecha_formateada = None
        return fecha_formateada
