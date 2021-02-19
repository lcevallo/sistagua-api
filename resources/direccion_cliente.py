import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request
from models.direccion_cliente import DireccionCliente

class DireccionClienteResource(Resource):
    def post(self):
        data = request.get_json()

        ficha_tecnica_object = self.find_by_cedula(data['cedula'],data['codigo'])
        if ficha_tecnica_object is not None:
            return {'mensaje': 'la ficha tecnica para ese usuario ya existe en la base de datos'}
        else:
            ficha_tecnica_id = self.insert(data)
            if ficha_tecnica_id:
                ficha_tecnica_object = self.buscar_x_id(ficha_tecnica_id)
                print(ficha_tecnica_object)
                return {'ficha_tecnica': ficha_tecnica_object}, HTTPStatus.CREATED


class DireccionClienteListResource(Resource):
    def get(self):
        column_where = []
        
        keys = [i for i in request.args.keys()]
        if len(keys) == 0:
            direcciones_list = self.buscar()            
        else:
            numeros = ['id','fk_provincia','fk_canton','fk_parroquia']
            varchars = ['direccion_domiciliaria','direccion_oficina','telefono_convencional']
            str1 = " "
            for key in keys:
                if key in numeros:
                    column_where.append((" AND direccion_cliente." + str(key) + " = {} ").format(request.args.get(key)))
                elif key in varchars:
                    column_where.append((" AND direccion_cliente." + str(key) + " like '%{}%' ").format(request.args.get(key)))
                elif key == 'cedula':
                    cedula=request.args.get(key)

            direcciones_list = self.buscar_x_criterio(str1.join(column_where))

        return {'direcciones_clientes': direcciones_list}, HTTPStatus.OK
    
    @classmethod
    def buscar_x_criterio(cls,cedula, criterio_where):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  direccion_cliente.* FROM direccion_cliente  INNER JOIN cliente_natural     ON direccion_cliente.fk_cliente = cliente_natural.id WHERE cliente_natural.ruc = {} AND cliente_natural.publish = TRUE AND direccion_cliente.publish = TRUE {}".format(cedula,criterio_where)
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []
        for row in rows:
            if row:
                direccion_cliente = DireccionCliente(
                    row['id'],
                    row['fk_cliente'],
                    row['fk_provincia'],
                    row['fk_canton'],
                    row['fk_parroquia'],
                    row['direccion_domiciliaria'],
                    row['direccion_oficina'],
                    row['telefono_convencional'],
                    row['publish']
                )
                data.append(direccion_cliente.data)

        return data

    @classmethod
    def buscar(cls):
        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        query = "SELECT  direccion_cliente.* FROM direccion_cliente  where direccion_cliente.publish = TRUE "
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        data = []

        for row in rows:
            if row:
                direccion_cliente = DireccionCliente(
                    row['id'],
                    row['fk_cliente'],
                    row['fk_provincia'],
                    row['fk_canton'],
                    row['fk_parroquia'],
                    row['direccion_domiciliaria'],
                    row['direccion_oficina'],
                    row['telefono_convencional'],
                    row['publish']
                )
                data.append(direccion_cliente.data)
        return data