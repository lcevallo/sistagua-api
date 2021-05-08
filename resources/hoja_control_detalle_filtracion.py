
import datetime
import re
from http import HTTPStatus

from flask import request
from flask_restful import Resource

import myconnutils
from models.hoja_control_detalle_filtracion import HojaControlDetalleFiltracion

class HojaControlDetalleFiltracionResource(Resource):
    def delete(self,id,fk_hc_detalle):
        hoja_control_detalle__filtracion_response = self.buscar_x_id(id,fk_hc_detalle)
       
        if hoja_control_detalle__filtracion_response:
            affected = self.borrarHojaControlDetalleFiltracion(id,fk_hc_detalle)
            if affected['hoja_control_detalle_filtracion_id'] > 0:
                return {'message': ''}, HTTPStatus.OK
            else:
                return {'message': f'No se pudo eliminar la filtracion  con id: {id} en esta hoja de control detalle: {fk_hc_detalle}'}, HTTPStatus.BAD_REQUEST
        else:
            return {'message': f'La filtracion  con id:{id}  en esta hoja de control detalle: {fk_hc_detalle} no fue encontrada en la base'}, HTTPStatus.NOT_FOUND

    @classmethod
    def buscar_x_id(cls, id, fk_hc_detalle):
        query = """
                SELECT
                    hoja_control_detalle_filtracion.id,
                    hoja_control_detalle_filtracion.fk_hoja_control_detalle,
                    hoja_control_detalle_filtracion.fk_filtracion,
                    hoja_control_detalle_filtracion.valor_filtracion,
                    hoja_control_detalle_filtracion.created_at,
                    hoja_control_detalle_filtracion.updated_at,
                    hoja_control_detalle_filtracion.publish,
                    hoja_control_detalle_filtracion.descripcion
                    FROM hoja_control_detalle_filtracion
                WHERE 
                    hoja_control_detalle_filtracion.id= %s
                    AND 
                    hoja_control_detalle_filtracion.fk_hoja_control_detalle = %s
                """
        
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        cursor.execute(query, (id,fk_hc_detalle))
        row = cursor.fetchone()
        connection.close()

        if row:
            hoja_control_detalle_filtracion = HojaControlDetalleFiltracion(
                    row['id'],
                    row['fk_hoja_control_detalle'],
                    row['fk_filtracion'],
                    row['valor_filtracion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish'],
                    row['descripcion']
                )
            return hoja_control_detalle_filtracion.data
        else:
            return None
    
    
    @classmethod
    def borrarHojaControlDetalleFiltracion(cls, id, fk_hc_detalle):
        query_delete = """
                        DELETE
                        FROM hoja_control_detalle_filtracion
                            WHERE id = %s
                        AND fk_hoja_control_detalle = %s
                        """
        
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        rows_afectada_detalle = cursor.execute(query_delete, (id,fk_hc_detalle))

        connection.commit()

        connection.close()
        return {'hoja_control_detalle_filtracion_id': rows_afectada_detalle}



class HojaControlDetalleFiltracionListResource(Resource):
    def get(self, fk_hc_detalle):
        filtraciones = self.buscar_filtraciones_x_hoja_control_detalle(fk_hc_detalle)
        return  {'hoja_control_detalle_filtracion': filtraciones}, HTTPStatus.OK
    
    @classmethod
    def buscar_filtraciones_x_hoja_control_detalle(cls, fk_hc_detalle):
        query ="""
            SELECT
                hoja_control_detalle_filtracion.id,
                hoja_control_detalle_filtracion.fk_hoja_control_detalle,
                hoja_control_detalle_filtracion.fk_filtracion,
                hoja_control_detalle_filtracion.valor_filtracion,
                hoja_control_detalle_filtracion.created_at,
                hoja_control_detalle_filtracion.updated_at,
                hoja_control_detalle_filtracion.publish,
                hoja_control_detalle_filtracion.descripcion
                FROM hoja_control_detalle_filtracion
            WHERE hoja_control_detalle_filtracion.fk_hoja_control_detalle = %s
        """
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        cursor.execute(query, (fk_hc_detalle,))
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                hoja_control_detalle_filtracion = HojaControlDetalleFiltracion(
                    row['id'],
                    row['fk_hoja_control_detalle'],
                    row['fk_filtracion'],
                    row['valor_filtracion'],
                    row['created_at'],
                    row['updated_at'],
                    row['publish'],
                    row['descripcion']
                )
                data.append(hoja_control_detalle_filtracion.data)

        return data