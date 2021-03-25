import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request, json

from models.cargos_vce import CargosVCE
from models.cliente_vce import ClienteVCE
from models.oficinas_vce import OficinasVCE


class VistaInfoClienteEmpresarialResource(Resource):
    def get(self):
        id = request.args.get('id')
        # id = data['id']
        cliente_empresarial = self.buscar_x_id(id)

        if not cliente_empresarial:
            return {'mensaje': f'Cliente con id {id} no existe en la base de datos.'}

        return {'data': cliente_empresarial}, HTTPStatus.OK

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        data = []
        data_ce = []
        data_oficinas = []
        data_cargos = []

        query_ce = '''
                        SELECT
                              cliente_empresarial.id,
                              cliente_empresarial.codigo,
                              cliente_empresarial.ruc,
                              cliente_empresarial.nombres,
                              cliente_empresarial.direccion,
                              cliente_empresarial.telefono,
                              cliente_empresarial.correo,
                              cliente_empresarial.publish
                            FROM cliente_empresarial
                            WHERE cliente_empresarial.id = %s
                    '''

        query_oficinas = '''
                                SELECT
                                  oficinas_empresa.id,
                                  oficinas_empresa.fk_cliente_empresarial,
                                  oficinas_empresa.fk_provincia,
                                  oficinas_empresa.fk_canton,
                                  oficinas_empresa.fk_parroquia,
                                  oficinas_empresa.sector,
                                  oficinas_empresa.direccion,
                                  oficinas_empresa.telefono_convencional,
                                  tbl_provincia.provincia,
                                  tbl_canton.canton,
                                  tbl_parroquia.parroquia
                                FROM oficinas_empresa
                                  LEFT OUTER JOIN tbl_provincia
                                    ON oficinas_empresa.fk_provincia = tbl_provincia.id
                                  INNER JOIN tbl_canton
                                    ON oficinas_empresa.fk_canton = tbl_canton.id
                                    AND tbl_canton.id_provincia = tbl_provincia.id
                                  INNER JOIN tbl_parroquia
                                    ON oficinas_empresa.fk_parroquia = tbl_parroquia.id
                                    AND tbl_parroquia.id_canton = tbl_canton.id
                                WHERE oficinas_empresa.fk_cliente_empresarial = %s
                                '''

        query_cargos = '''
                        SELECT
                          contactos_empresa.id,
                          cargo.nombres,
                          cargo.apellidos,
                          cargo.celular,
                          cargo.cumple,
                          cargo.correo,
                          tipo_cargo.tipo,
                          contactos_empresa.fk_cliente_empresarial,
                          contactos_empresa.fk_cargo
                        
                        FROM cargo
                          LEFT OUTER JOIN tipo_cargo
                            ON cargo.fk_tipo_cargo = tipo_cargo.id
                          RIGHT OUTER JOIN contactos_empresa
                            ON contactos_empresa.fk_cargo = cargo.id
                        WHERE contactos_empresa.fk_cliente_empresarial = %s        
                    '''

        cursor.execute(query_ce, (id,))
        row = cursor.fetchone()

        if row:
            clienteVCE = ClienteVCE(
                row['id'],
                row['codigo'],
                row['ruc'],
                row['nombres'],
                row['direccion'],
                row['telefono'],
                row['correo'],
                row['publish']
            )
            data_ce.append(clienteVCE.data)

        else:
            return data

        cursor.execute(query_oficinas, (id,))
        rows = cursor.fetchall()

        for row in rows:
            if row:
                oficinasVCE = OficinasVCE(
                    row['id'],
                    row['fk_cliente_empresarial'],
                    row['fk_provincia'],
                    row['fk_canton'],
                    row['fk_parroquia'],
                    row['sector'],
                    row['direccion'],
                    row['telefono_convencional'],
                    row['provincia'],
                    row['canton'],
                    row['parroquia']
                )
                data_oficinas.append(oficinasVCE.data)

        cursor.execute(query_cargos, (id,))
        rows = cursor.fetchall()

        for row in rows:
            if row:
                cargosVCE = CargosVCE(
                    row['id'],
                    row['nombres'],
                    row['apellidos'],
                    row['celular'],
                    row['cumple'],
                    row['correo'],
                    row['tipo'],
                    row['fk_cliente_empresarial'],
                    row['fk_cargo']
                )
                data_cargos.append(cargosVCE.data)

        connection.close()

        return {
            'cliente_empresarial': data_ce,
            'oficinas': data_oficinas,
            'cargos': data_cargos
        }
