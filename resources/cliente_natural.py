import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request
from models.cliente_natural import Cliente_Natural
import json


class ClienteNaturalResource(Resource):
    def get(self):
        cedula = request.args.get('cedula')
        ruc = request.args.get('ruc')
        if ruc:
            cliente = self.find_by_cedula(ruc)
        else:
            cliente = self.find_by_cedula(cedula)

        if cliente:
            return cliente
        return {'mensaje': 'Cliente no encontrado'}, 404

    def post(self):
        data = request.get_json()
        
        cliente_id = self.insert_by_stored_procedure(data)
        
        return {'cliente': cliente_id}, HTTPStatus.CREATED

        # cliente_object = self.find_by_cedula(data['cedula'])
        # if cliente_object is not None:
        #     return {'mensaje': 'El cliente ya existe en la base de datos'}
        # else:
        #     cliente_id = self.insert(data)
        #     if cliente_id:
        #         cliente_object = self.buscar_x_id(cliente_id)
        #         print(cliente_object)
        #         return {'cliente': cliente_object}, HTTPStatus.CREATED

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
        query = '''SELECT
                    cliente_ficha.*
                    FROM cliente_natural                  
                    WHERE ruc = %s AND publish= true
                '''
        cursor.execute(query, (cedula,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cliente_natural = Cliente_Natural(
                row['id'],
                row['codigo'],
                row['ruc'],
                row['nombre1'],
                row['nombre2'],
                row['apellido1'],
                row['apellido2'],
                row['correo'],
                row['celular'],
                row['cumple'],
                row['foto'],
                row['publish']
            )
            return cliente_natural.data
        else:
            return None

    @classmethod
    def buscar_x_id(cls, id):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """
                SELECT
                *
                FROM cliente_natural
                WHERE id = %s AND publish= true
                """
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            cliente_natural = Cliente_Natural(
                row['id'],
                row['codigo'],
                row['ruc'],
                row['nombre1'],
                row['nombre2'],
                row['apellido1'],
                row['apellido2'],
                row['correo'],
                row['celular'],
                row['cumple'],
                row['foto'],
                row['publish']
            )
            return cliente_natural.data
        else:
            return None

    @classmethod
    def insert(cls, valor):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()
        query_insert = """
                        INSERT INTO cliente_natural (correo, nombre, apellidos, cedula, telefono, created_at)
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
    def insert_by_stored_procedure(cls, v_json):
        
        connection = myconnutils.getConnection()
        cursor = connection.cursor()


        cliente_natural=json.dumps(v_json['cliente_natural'])
        parentesco=json.dumps(v_json['parentesco'])
        direcciones=json.dumps(v_json['direcciones'])
        
        print(cliente_natural)
        print(parentesco)
        print(direcciones)

        
        query_stored_procedure="CALL lc_sp_guardar_cliente_natural(%s,%s,%s,@json_respuesta)"
        query_respuesta="Select @json_respuesta"


        cursor.execute(query_stored_procedure,(cliente_natural,parentesco,direcciones))
        cursor.execute(query_respuesta)
        row = cursor.fetchone()

        # args = ["""
        #         '[{ "codigo": "C0001",
        #                                 "ruc": "0705114775",
        #                                 "apellido1": "Cerezo",
        #                                 "apellido2": "",
        #                                 "nombre1": "CArlos",
        #                                 "nombre2": "",
        #                                 "celular": "0994898148",
        #                                 "correo": "",
        #                                 "cumple": "1990-04-24",
        #                                 "foto": ""
        #                             }]'
        #             """             
        #                         ,
        #             """
        #                         '[{
        #                             "tipo_parentesco": "sdfsdf",
        #                             "sexo": "M",
        #                             "nombre1": "",
        #                             "nombre2": "",
        #                             "apellido1": "dfsdf",
        #                             "apellido2": "",
        #                             "celular": "fsdfsdfsdf",
        #                             "correo": "fsdfsdfsdf",
        #                             "cumple": ""
        #                             },
        #                             {
        #                             "tipo_parentesco": "sdfsdf",
        #                             "sexo": "M",
        #                             "nombre1": "",
        #                             "nombre2": "",
        #                             "apellido1": "dfsdf",
        #                             "apellido2": "",
        #                             "celular": "fsdfsdfsdf",
        #                             "correo": "fsdfsdfsdf",
        #                             "cumple": ""
        #                         }]'
        #             """                
        #                             ,
        #             """
        #                         '[{
        #                             "fk_provincia": 3,
        #                             "fk_canton": 27,
        #                             "fk_parroquia": 175,
        #                             "direccion_domiciliaria": "Vía Arcapamba",
        #                             "direccion_oficina": "",
        #                             "telefono_convencional": ""
        #                         }]'
        #             """, 
        #                             0]

        # result_args = cursor.callproc('lc_sp_guardar_cliente_natural', args)

        # print(result_args[3])

        connection.commit()
        
        connection.close()

        return row['@json_respuesta']
        
    
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


class ClientesNaturalesListResource(Resource):

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

            print(column_where)
            clientes_list = self.buscar_x_criterio(str1.join(column_where))

        return {'clientes': clientes_list}, HTTPStatus.OK
        # return clientes_list, HTTPStatus.OK

    @classmethod
    def buscar_x_criterio(cls, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT * from cliente_natural where publish = true {}".format(criterio_where)
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                cliente_natural = Cliente_Natural(
                    row['id'],
                    row['codigo'],
                    row['ruc'],
                    row['nombre1'],
                    row['nombre2'],
                    row['apellido1'],
                    row['apellido2'],
                    row['correo'],
                    row['celular'],
                    row['cumple'],
                    row['foto'],
                    row['publish']
                )
                data.append(cliente_natural.data)

        connection.close()
        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = """SELECT
                      *
                    FROM cliente_natural
                    WHERE cliente_natural.publish = TRUE
                """

        cursor.execute(query)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            if row:
                cliente_natural = Cliente_Natural(
                    row['id'],
                    row['codigo'],
                    row['ruc'],
                    row['nombre1'],
                    row['nombre2'],
                    row['apellido1'],
                    row['apellido2'],
                    row['correo'],
                    row['celular'],
                    row['cumple'],
                    row['foto'],
                    row['publish']
                )
                data.append(cliente_natural.data)

        connection.close()
        return data