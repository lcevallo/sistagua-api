import myconnutils
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask import request, json
from models.cliente_empresarial import ClienteEmpresarial
from models.contactos_empresa import ContactosEmpresa
from models.oficinas_empresa import OficinasEmpresa
import re, datetime


class MasterDetailCEResource(Resource):
    def post(self):
        data = request.get_json()
        ids_ingresados = self.sp_ingresar_cliente_empresarial_master_detail(data)
        return ids_ingresados

    @classmethod
    def sp_ingresar_cliente_empresarial_master_detail(cls, v_json):
        cliente_empresarial = v_json['cliente_empresarial']
        contactos = v_json['contactos']
        oficinas = v_json['oficinas']

        contactos_size = len(contactos)
        oficinas_size = len(oficinas)

        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        # primero agrego  el cliente empresarial
        # y obtengo el id        
        query_insert_ce = """
                            INSERT INTO cliente_empresarial (codigo, ruc, nombres, direccion, telefono, correo)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """

        query_existe_cliente_empresarial_codigo = """
                                            SELECT
                                            1 AS existe
                                            FROM cliente_empresarial
                                            WHERE cliente_empresarial.codigo = %s
                                            AND  cliente_empresarial.publish=true
                                            """

        query_existe_cliente_empresarial_ruc = """
                                            SELECT
                                            1 AS existe
                                            FROM cliente_empresarial
                                            WHERE cliente_empresarial.ruc = %s
                                            AND  cliente_empresarial.publish=true
                                            """

        codigo = cliente_empresarial["codigo"]
        ruc = cliente_empresarial["ruc"]

        cursor.execute(query_existe_cliente_empresarial_codigo, (codigo,))
        row_codigo = cursor.fetchone()

        cursor.execute(query_existe_cliente_empresarial_ruc, (ruc,))
        row_ruc = cursor.fetchone()

        if row_codigo:
            connection.close()
            return {'mensaje': f"El cliente con el codigo {codigo} ya se encuentra en la base de datos"}

        if row_ruc:
            connection.close()
            return {'mensaje': f"El cliente con el codigo {ruc} ya se encuentra en la base de datos"}

        cursor.execute(query_insert_ce,
                       (
                           cliente_empresarial["codigo"],
                           cliente_empresarial["ruc"],
                           cliente_empresarial["nombres"],
                           cliente_empresarial["direccion"],
                           cliente_empresarial["telefono"],
                           cliente_empresarial["correo"]
                       )
                       )

        connection.commit()
        id_cliente_empresarial_inserted = cursor.lastrowid

        # Aqui agrego las direcciones de la oficina        
        ids_oficinas_empresa = []
        query_insert_oficina = """
                                    INSERT INTO oficinas_empresa (fk_cliente_empresarial,fk_provincia, fk_canton, fk_parroquia, sector, direccion, telefono_convencional)
                                    VALUES (%s,%s, %s, %s, %s, %s, %s)
                                    """

        for index_ofi in range(oficinas_size):
            cursor.execute(query_insert_oficina,
                           (
                               id_cliente_empresarial_inserted,
                               oficinas[index_ofi]["fk_provincia"],
                               oficinas[index_ofi]["fk_canton"],
                               oficinas[index_ofi]["fk_parroquia"],
                               oficinas[index_ofi]["sector"],
                               oficinas[index_ofi]["direccion"],
                               oficinas[index_ofi]["telefono_convencional"]
                           )
                           )

            connection.commit()
            ids_oficinas_empresa.append(cursor.lastrowid)

        # Aqui agrego los contactos de la empresa    
        ids_contactos_empresa = []
        query_insert_contactos = """
                                    INSERT INTO contactos_empresa (fk_cliente_empresarial, fk_cargo)
                                    VALUES (%s, %s)
                                    """

        query_cargo_ce = """
                            INSERT INTO cargo (fk_tipo_cargo, nombres, apellidos, celular,cumple, correo)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
        query_cargo_ce_sin_cumple = """
                            INSERT INTO cargo (fk_tipo_cargo, nombres, apellidos, celular, correo)
                            VALUES (%s, %s, %s, %s, %s)
                        """

        query_verificar_existe_cargo = """
                                         SELECT 1 AS hay
                                            FROM cargo
                                            WHERE cargo.id = %s AND publish=true                    
                                        """

        for index_contacto in range(contactos_size):

            if not contactos[index_contacto]["cumple"]:
                # Debo de usar sin cumple
                cursor.execute(query_cargo_ce_sin_cumple,
                               (
                                   contactos[index_contacto]["fk_tipo_cargo"],
                                   contactos[index_contacto]["nombres"],
                                   contactos[index_contacto]["apellidos"],
                                   contactos[index_contacto]["celular"],
                                   contactos[index_contacto]["correo"]
                               )
                               )
            else:
                # Debo de usar con cumple
                fecha_cumple = re.search('\d{4}-\d{2}-\d{2}', contactos[index_contacto]["cumple"])
                fecha_formateada = datetime.datetime.strptime(fecha_cumple.group(), '%Y-%m-%d').date()
                cursor.execute(query_cargo_ce,
                               (
                                   contactos[index_contacto]["fk_tipo_cargo"],
                                   contactos[index_contacto]["nombres"],
                                   contactos[index_contacto]["apellidos"],
                                   contactos[index_contacto]["celular"],
                                   fecha_formateada,
                                   contactos[index_contacto]["correo"]
                               )
                               )

            connection.commit()
            v_fk_cargo = cursor.lastrowid

            # TODO: agregar en la tabla contactos_empresa con el ultimo id que se envio
            cursor.execute(query_verificar_existe_cargo, (v_fk_cargo,))
            row = cursor.fetchone()

            if row:

                cursor.execute(query_insert_contactos,
                               (
                                   id_cliente_empresarial_inserted,
                                   v_fk_cargo
                               )
                               )

                connection.commit()
                ids_contactos_empresa.append(cursor.lastrowid)
            else:
                ids_contactos_empresa.append(f"No existe un cargo con el siguiente id: {v_fk_cargo}")

        connection.close()

        return {
            'id_cliente_empresarial': id_cliente_empresarial_inserted,
            'ids_oficinas': ids_oficinas_empresa,
            'ids_contactos': ids_contactos_empresa
        }

    @classmethod
    def sp_actualizar_cliente_empresarial_master_detail(cls, v_json):
        cliente_empresarial = v_json['cliente_empresarial']
        contactos = v_json['contactos']
        oficinas = v_json['oficinas']

        contactos_size = len(contactos)
        oficinas_size = len(oficinas)

        connection = myconnutils.getConnection()
        cursor = connection.cursor()

        # primero actualizo el cliente empresarial

        id_cliente_empresarial_updated = cliente_empresarial["id"]
        query_update_ce = """
                            UPDATE cliente_empresarial
                                SET codigo = %s,
                                    ruc = %s,
                                    nombres = %s,
                                    direccion = %s,
                                    telefono = %s,
                                    correo = %s,
                                    updated_at = CURRENT_TIMESTAMP()
                                WHERE id = %s
                                AND publish = true
                          """
        cursor.execute(query_update_ce,
                       (
                           cliente_empresarial["codigo"],
                           cliente_empresarial["ruc"],
                           cliente_empresarial["nombres"],
                           cliente_empresarial["direccion"],
                           cliente_empresarial["telefono"],
                           cliente_empresarial["correo"],
                           id_cliente_empresarial_updated
                       )
                       )

        connection.commit()

        afectados_ce = cursor.rowcount

        afectados_ce_oficinas_empresa = []
        query_insert_oficina = """
                                    UPDATE oficinas_empresa
                                    SET fk_provincia = %s,
                                        fk_canton = %s,
                                        fk_parroquia = %s,
                                        sector = %s,
                                        direccion = %s,
                                        telefono_convencional = %s,
                                        updated_at = CURRENT_TIMESTAMP()
                                    WHERE id = %s
                                    AND fk_cliente_empresarial = %s
                                    AND publish = TRUE
                                    """

        # segundo recorro el array del json de las oficinas
        for index_ofi in range(oficinas_size):
            cursor.execute(query_insert_oficina,
                           (
                               oficinas[index_ofi]["fk_provincia"],
                               oficinas[index_ofi]["fk_canton"],
                               oficinas[index_ofi]["fk_parroquia"],
                               oficinas[index_ofi]["sector"],
                               oficinas[index_ofi]["direccion"],
                               oficinas[index_ofi]["telefono_convencional"],
                               oficinas[index_ofi]["id"],
                               id_cliente_empresarial_updated
                           )
                           )

            connection.commit()
            afectados_ce_oficinas_empresa.append(cursor.rowcount)

        # Aqui agrego los contactos de la empresa    
        afectados_ce_contactos_empresa = []
        query_updates_contactos = """
                                        UPDATE contactos_empresa
                                            SET fk_cargo = %s,
                                                updated_at = CURRENT_TIMESTAMP()
                                            WHERE id = %s
                                            AND fk_cliente_empresarial = %s AND publish=true  
                                """

        query_verificar_existe_cargo = """
                                         SELECT 1 AS hay
                                            FROM cargo
                                            WHERE cargo.id = %s AND publish=true                    
                                        """

        for index_contacto in range(contactos_size):
            # TODO: verificar si existe en base ese cargo

            cursor.execute(query_verificar_existe_cargo, (contactos[index_contacto]["fk_cargo"],))
            row = cursor.fetchone()
            v_fk_cargo = contactos[index_contacto]["fk_cargo"]

            if row:
                cursor.execute(query_updates_contactos,
                               (
                                   contactos[index_contacto]["fk_cargo"],
                                   id_cliente_empresarial_updated,
                                   contactos[index_contacto]["fk_cliente_empresarial"]
                               )
                               )

                connection.commit()
                afectados_ce_contactos_empresa.append(cursor.rowcount)
            else:
                afectados_ce_contactos_empresa.append(f"No existe un cargo con el siguiente id: {v_fk_cargo}")
