from http import HTTPStatus
from models.contactos_ce import ContactosEmpresaV

import myconnutils
from flask_restful import Resource, reqparse
from flask import request

import re, datetime


class ContactoCEResource(Resource):
    def put(self):
        data = request.get_json()
        id = data['id']
        obj_x_id = self.buscar_x_id(data['id'])
        if obj_x_id:
            cant_registros = self.actualizar(data)
            if cant_registros > 0:
                return {'respuesta': f'El registro con {id} se ha actulizado de manera correcta'}, HTTPStatus.CREATED
            else:
                return {'respuesta': f'El registro con {id} no se actualizo'}, HTTPStatus.BAD_REQUEST
        else:
            return {'respuesta': f'El registro con {id} no existe en base!'}, HTTPStatus.BAD_REQUEST

    def delete(self):
        id = request.args.get('id')
        fk_cargo = request.args.get('fkCargo')
        contactos_response = self.buscar_x_id(id)
        if contactos_response:
            affected = self.eliminar(id, fk_cargo)
            if affected == 0:
                return {'message': ''}, HTTPStatus.OK
            else:
                return {'message': f'No se pudo eliminar este cargo con id: {id}'}, HTTPStatus.BAD_REQUEST
        else:
            return {'message': 'cargo con id no encontrada en la base'}, HTTPStatus.NOT_FOUND



    @classmethod
    def actualizar(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        if valor['cumple']:
            fecha_cumple = re.search('\d{4}-\d{2}-\d{2}', valor['cumple'])
            fecha_formateada = datetime.datetime.strptime(fecha_cumple.group(), '%Y-%m-%d').date()
        else:
            fecha_formateada = None

        query_update = '''
                        UPDATE cargo
                            SET fk_tipo_cargo = %s,
                                nombres = %s,
                                apellidos = %s,
                                celular = %s,
                                cumple = %s,
                                correo = %s
                              WHERE
                              id = %s
                        '''

        rows_afectada= cursor.execute(query_update, (
                                    valor['fkTipoCargo'],
                                    (valor['nombres']).strip(),
                                    (valor['apellidos']).strip(),
                                    (valor['celular']).strip(),
                                    fecha_formateada,
                                    (valor['correo']).strip(),
                                    valor['fkCargo']
                                )
                       )
        connection.commit()
        # rows_afectada = cursor.lastrowid
        connection.close()
        return rows_afectada

    @classmethod
    def eliminar(cls, id_ce, id_cargo):
        query_delete_ce = """
                            DELETE
                                FROM contactos_empresa
                                WHERE contactos_empresa.id = %s
                            """
        query_delete_cargo = """
                            DELETE
                                FROM cargo
                                WHERE cargo.id = %s
                            """
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        rows_afectada = cursor.execute(query_delete_ce, (id_ce,))

        cursor.execute(query_delete_cargo, (id_cargo,))
        connection.commit()

        connection.close()
        return rows_afectada

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query = """
               SELECT
                  contactos_empresa.id,
                  contactos_empresa.fk_cliente_empresarial,
                  contactos_empresa.fk_cargo,
                  contactos_empresa.publish,
                  cargo.nombres,
                  cargo.apellidos,
                  cargo.celular,
                  cargo.cumple,
                  cargo.correo,
                  cargo.fk_tipo_cargo
                FROM contactos_empresa
                  LEFT OUTER JOIN cargo
                    ON contactos_empresa.fk_cargo = cargo.id
                  
                  WHERE
                    contactos_empresa.id=%s
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            contactos_ce = ContactosEmpresaV(
                row['id'],
                row['fk_cliente_empresarial'],
                row['fk_cargo'],
                row['publish'],
                row['nombres'],
                row['apellidos'],
                row['celular'],
                row['cumple'],
                row['correo'],
                row['fk_tipo_cargo']
            )
            return contactos_ce.data
        else:
            return None


class ContactosListCEResource(Resource):
    def get(self, fk_cliente):
        contactos_list = self.find_all_by_cliente(fk_cliente)

        if contactos_list is None:
            return {'mensaje': 'No existen contactos para este cliente empresarial'}, HTTPStatus.NOT_FOUND

        return {'contactos': contactos_list}

    @classmethod
    def find_all_by_cliente(cls, fk_cliente):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query = '''
                    SELECT
                      contactos_empresa.id,
                      contactos_empresa.fk_cliente_empresarial,
                      contactos_empresa.fk_cargo,
                      contactos_empresa.publish,
                      cargo.nombres,
                      cargo.apellidos,
                      cargo.celular,
                      cargo.cumple,
                      cargo.correo,
                      cargo.fk_tipo_cargo
                    FROM contactos_empresa
                      LEFT OUTER JOIN cargo
                        ON contactos_empresa.fk_cargo = cargo.id  
                      WHERE
                        contactos_empresa.fk_cliente_empresarial=%s
                    '''

        cursor.execute(query, (fk_cliente,))
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                contactos_ce = ContactosEmpresaV(
                    row['id'],
                    row['fk_cliente_empresarial'],
                    row['fk_cargo'],
                    row['publish'],
                    row['nombres'],
                    row['apellidos'],
                    row['celular'],
                    row['cumple'],
                    row['correo'],
                    row['fk_tipo_cargo']
                )
                data.append(contactos_ce.data)

        return data
