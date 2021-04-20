import datetime
import re
from http import HTTPStatus

from flask import request
from flask_restful import Resource

import myconnutils
from models.ficha_tecnica import FichaTecnica
from models.hoja_control import HojaControl
from models.hoja_control_detalle import HojaControlDetalle
from models.temp.hoja_control_tmp import HojaControlTMP


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


class HojaControlResource(Resource):
    def get(self, id):
        hoja_control = self.buscar_x_id(id)
        detalle_items = self.buscar_detalle_x_id(id)
        return {'hoja_control': hoja_control, 'itemDetale': detalle_items}, HTTPStatus.OK

    def delete(self, id):
        hoja_control_response = self.buscar_x_id(id)
        if hoja_control_response:
            affected = self.borrarHojaControl(id)
            if affected['hoja_control_id'] > 0:
                return {'message': ''}, HTTPStatus.OK
            else:
                return {'message': f'No se pudo eliminar la hoja de control con id: {id}'}, HTTPStatus.BAD_REQUEST
        else:
            return {'message': f'Hoja de control con id:{id} no encontrada en la base'}, HTTPStatus.NOT_FOUND

    @classmethod
    def borrarHojaControl(cls, id):
        query_delete_hoja_control = """
            DELETE
                FROM hoja_control
            WHERE
                id = %s
        """

        query_delete_hoja_control_detalle = """
            DELETE
                FROM hoja_control_detalle
            WHERE
                fk_hoja_control = %s
        """
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        rows_afectada_detalle = cursor.execute(query_delete_hoja_control_detalle, (id,))

        rows_afectada = cursor.execute(query_delete_hoja_control, (id,))
        connection.commit()

        connection.close()
        return {'hoja_control_id': rows_afectada, 'ids_detalles': rows_afectada_detalle}

    @classmethod
    def getFechaFormateada(cls, fecha_no_formateada):
        if fecha_no_formateada:
            fecha_comprado = re.search('\d{4}-\d{2}-\d{2}', fecha_no_formateada)
            fecha_formateada = datetime.datetime.strptime(fecha_comprado.group(), '%Y-%m-%d').date()
        else:
            fecha_formateada = None
        return fecha_formateada

    @classmethod
    def buscar_x_id(cls, id):

        query = """
                    SELECT
                      hoja_control.id,
                      hoja_control.fk_cliente,
                      hoja_control.tipo_cliente,
                      hoja_control.codigo,
                      hoja_control.tds,
                      hoja_control.ppm,
                      hoja_control.visitas,
                      hoja_control.fecha_comprado,
                      hoja_control.created_at,
                      hoja_control.updated_at,
                      hoja_control.publish
                    FROM hoja_control
                    WHERE hoja_control.id = %s
                  """

        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            hoja_control = HojaControl(
                row['id'],
                row['fk_cliente'],
                row['tipo_cliente'],
                row['codigo'],
                row['tds'],
                row['ppm'],
                row['visitas'],
                row['fecha_comprado'],
                row['created_at'],
                row['updated_at'],
                row['publish']
            )
            return hoja_control.data
        else:
            return None

    @classmethod
    def buscar_detalle_x_id(cls, id):
        query = """
                    SELECT
                      hoja_control_detalle.id,
                      hoja_control_detalle.fk_hoja_control,
                      hoja_control_detalle.factura,
                      hoja_control_detalle.fecha_mantenimiento,
                      hoja_control_detalle.recibo,
                      hoja_control_detalle.hoja_control,
                      hoja_control_detalle.descripcion,
                      hoja_control_detalle.persona_autoriza,
                      hoja_control_detalle.firma_url,
                      hoja_control_detalle.cedula_autoriza,
                      hoja_control_detalle.persona_dio_mantenimiento,
                      hoja_control_detalle.cedula_dio_mantenimiento,
                      hoja_control_detalle.ppm,
                      hoja_control_detalle.tds,
                      hoja_control_detalle.created_at,
                      hoja_control_detalle.updated_at,
                      hoja_control_detalle.publish
                    FROM hoja_control_detalle
                      WHERE
                      hoja_control_detalle.fk_hoja_control = %s
                """

        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                hoja_control_detalle = HojaControlDetalle(
                    row['id'],
                    row['fk_hoja_control'],
                    row['factura'],
                    row['fecha_mantenimiento'],
                    row['recibo'],
                    row['hoja_control'],
                    row['descripcion'],
                    row['persona_autoriza'],
                    row['firma_url'],
                    row['cedula_autoriza'],
                    row['persona_dio_mantenimiento'],
                    row['cedula_dio_mantenimiento'],
                    row['ppm'],
                    row['tds'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish']
                )
                data.append(hoja_control_detalle.data)

        return data


class HojasControlListResource(Resource):
    def get(self):
        hojas_control = self.traer_hojas_control()
        return {'hojas_control': hojas_control}, HTTPStatus.OK

    def post(self):
        json_data = request.get_json()
        detalle_items = json_data['detalle']
        del json_data['detalle']
        return self.guardar(json_data, detalle_items)

    @classmethod
    def traer_hojas_control(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                    SELECT
                          hoja_control.id,
                          hoja_control.codigo,
                          hoja_control.fk_cliente, 
                          CASE hoja_control.tipo_cliente
                              WHEN 1 THEN (SELECT CONCAT_WS(' ',cn.nombre1, cn.nombre2, cn.apellido1, cn.apellido2) FROM cliente_natural cn WHERE cn.id= hoja_control.fk_cliente)
                              WHEN 2 THEN (SELECT CONCAT_WS(' ',ce.nombres) FROM cliente_empresarial ce WHERE ce.id= hoja_control.fk_cliente)
                              ELSE NULL
                          END as 'cliente',
                          hoja_control.tipo_cliente,
                          hoja_control.tds,
                          hoja_control.ppm,
                          hoja_control.visitas,
                          hoja_control.fecha_comprado
                        FROM hoja_control
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                hoja_control_tmp = HojaControlTMP(
                    row['id'],
                    row['codigo'],
                    row['fk_cliente'],
                    row['cliente'],
                    row['tipo_cliente'],
                    row['tds'],
                    row['ppm'],
                    row['visitas'],
                    row['fecha_comprado']
                )
                data.append(hoja_control_tmp.data)
        return data

    @classmethod
    def guardar(cls, hoja_control_json, hoja_control_detalle_json):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        fecha_comprado = cls.getFechaFormateada(hoja_control_json['fecha_comprado'])

        query_hoja_control_insert = """
                            INSERT INTO hoja_control(fk_cliente, tipo_cliente, codigo, tds, ppm, visitas, fecha_comprado)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                       """
        query_hoja_control_update = """
                                    UPDATE hoja_control
                                        SET fk_cliente = %s,
                                            tipo_cliente = %s,
                                            codigo = %s,
                                            tds = %s,
                                            ppm = %s,
                                            visitas = %s,
                                            fecha_comprado = %s,
                                            updated_at = CURRENT_TIMESTAMP(),
                                            publish = true
                                    WHERE id = %s
                                """

        query_hoja_control_detalle_insert = """
                                INSERT INTO hoja_control_detalle (fk_hoja_control, factura, fecha_mantenimiento, recibo, hoja_control, descripcion, persona_autoriza, firma_url, cedula_autoriza, persona_dio_mantenimiento, cedula_dio_mantenimiento,ppm,tds)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                                """

        query_hoja_control_detalle_update = """
                                    UPDATE hoja_control_detalle
                                    SET factura = %s,
                                        fecha_mantenimiento = %s,
                                        recibo = %s,
                                        hoja_control = %s,
                                        descripcion = %s,
                                        persona_autoriza = %s,
                                        firma_url = %s,
                                        cedula_autoriza = %s,
                                        persona_dio_mantenimiento = %s,
                                        cedula_dio_mantenimiento = %s,
                                        ppm = %s,
                                        tds = %s,
                                        updated_at = CURRENT_TIMESTAMP()
                                    WHERE id = %s
                                    AND fk_hoja_control = %s
                                """
        query_hoja_control_detalle_delete = """
                                                DELETE
                                                    FROM hoja_control_detalle
                                                WHERE id = %s
                                                    AND fk_hoja_control = %s
                                            """

        if 'id' in hoja_control_json:
            cursor.execute(query_hoja_control_update, (
                hoja_control_json['fk_cliente'],
                hoja_control_json['tipo_cliente'],
                hoja_control_json['codigo'],
                hoja_control_json['tds'],
                hoja_control_json['ppm'],
                hoja_control_json['visitas'],
                fecha_comprado,
                hoja_control_json['id']
            )
                           )
            id_hoja_control = hoja_control_json['id']

        else:
            cursor.execute(query_hoja_control_insert, (
                hoja_control_json['fk_cliente'],
                hoja_control_json['tipo_cliente'],
                hoja_control_json['codigo'],
                hoja_control_json['tds'],
                hoja_control_json['ppm'],
                hoja_control_json['visitas'],
                fecha_comprado
            )
                           )
            id_hoja_control = cursor.lastrowid

        insert_ids = []
        connection.commit()

        for row in hoja_control_detalle_json:
            if row:
                # if row['id'] is None or row['fk_hoja_control'] == 0:
                if 'id' in row:
                    valor_ppm = None;
                    if 'ppm' in row:
                        valor_ppm = row['ppm']

                    valor_tds = None;
                    if 'tds' in row:
                        valor_tds = row['tds']

                    cursor.execute(query_hoja_control_detalle_update,
                                   (
                                       (row['factura']).strip(),
                                       cls.getFechaFormateada(row['fecha_mantenimiento']),
                                       (row['recibo']).strip(),
                                       (row['hoja_control']).strip(),
                                       (row['descripcion']).strip(),
                                       (row['persona_autoriza']).strip(),
                                       (row['firma_url']).strip(),
                                       (row['cedula_autoriza']).strip(),
                                       (row['persona_dio_mantenimiento']).strip(),
                                       (row['cedula_dio_mantenimiento']).strip(),
                                       row['ppm'],
                                       row['tds'],
                                       row['id'],
                                       row['fk_hoja_control']
                                   )
                                   )
                    insert_ids.append(row['id'])
                else:
                    valor_ppm = None;
                    if 'ppm' in row:
                        valor_ppm = row['ppm']

                    valor_tds = None;
                    if 'tds' in row:
                        valor_tds = row['tds']

                    cursor.execute(query_hoja_control_detalle_insert,
                                   (
                                       id_hoja_control,
                                       (row['factura']).strip(),
                                       cls.getFechaFormateada(row['fecha_mantenimiento']),
                                       (row['recibo']).strip(),
                                       (row['hoja_control']).strip(),
                                       (row['descripcion']).strip(),
                                       (row['persona_autoriza']).strip(),
                                       (row['firma_url']).strip(),
                                       (row['cedula_autoriza']).strip(),
                                       (row['persona_dio_mantenimiento']).strip(),
                                       (row['cedula_dio_mantenimiento']).strip(),
                                       valor_ppm,
                                       valor_tds
                                   )
                                   )
                    insert_ids.append(cursor.lastrowid)

            connection.commit()

        # Para los que elimino
        if 'deletedHojaControlItemIds' in hoja_control_json:
            deleted_hoja_control_items_id = hoja_control_json['deletedHojaControlItemIds']
            ids_borrar = deleted_hoja_control_items_id.split(',')

            for id_hoja_control_detalle in ids_borrar:
                cursor.execute(query_hoja_control_detalle_delete, (id_hoja_control_detalle, id_hoja_control))
                connection.commit()

        connection.close()
        return {'id_hoja_control': id_hoja_control, 'ids_detalles': insert_ids}

    @classmethod
    def getFechaFormateada(cls, fecha_no_formateada):
        if fecha_no_formateada:
            fecha_comprado = re.search('\d{4}-\d{2}-\d{2}', fecha_no_formateada)
            fecha_formateada = datetime.datetime.strptime(fecha_comprado.group(), '%Y-%m-%d').date()
        else:
            fecha_formateada = None
        return fecha_formateada
