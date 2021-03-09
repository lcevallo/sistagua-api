 # ------------------------------------->INICIO PARENTESCO<----------------------------------------------

        sql_update_cn_parentesco_con_cumple = """
                                        UPDATE parentesco
                                        SET tipo_parentesco = %s,
                                            sexo = %s,
                                            nombre1 = %s,
                                            nombre2 = %s,
                                            apellido1 = %s,
                                            apellido2 = %s,
                                            celular = %s,
                                            correo = %s,
                                            cumple = %s
                                        WHERE id = %s
                                        AND fk_cliente = %s
                                        AND publish = true
                                    """

        sql_insert_cn_parentesco_con_cumple = """
                                        INSERT INTO parentesco (fk_cliente, tipo_parentesco, sexo, nombre1, nombre2, apellido1, apellido2, celular, correo, cumple)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                                
        sql_update_cn_parentesco_sin_cumple = """
                                        UPDATE parentesco
                                        SET tipo_parentesco = %s,
                                            sexo = %s,
                                            nombre1 = %s,
                                            nombre2 = %s,
                                            apellido1 = %s,
                                            apellido2 = %s,
                                            celular = %s,
                                            correo = %s                                            
                                        WHERE id = %s
                                        AND fk_cliente = %s
                                        AND publish = true
                                    """

        sql_insert_cn_parentesco_sin_cumple = """
                                        INSERT INTO parentesco (fk_cliente, tipo_parentesco, sexo, nombre1, nombre2, apellido1, apellido2, celular, correo)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """

        ids_parentesco = []
        for index_parentesco in range(parentesco_size):
            
            if len(str(parentesco[index_parentesco]["id"])) == 0:
                
                if not parentesco[index_parentesco]["cumple"]:
                    # Debo de usar sin cumple
                    cursor.execute(sql_insert_cn_parentesco_sin_cumple,
                               (
                                   fk_cliente_inserted,
                                   parentesco[index_parentesco]["tipo_parentesco"],
                                   parentesco[index_parentesco]["sexo"],
                                   parentesco[index_parentesco]["nombre1"],
                                   parentesco[index_parentesco]["nombre2"],
                                   parentesco[index_parentesco]["apellido1"],
                                   parentesco[index_parentesco]["apellido2"],
                                   parentesco[index_parentesco]["celular"],
                                   parentesco[index_parentesco]["correo"]
                               )
                               )                    
                else:
                    # Debo de usar con cumple
                    fecha_cumple = datetime.datetime.strptime(parentesco[index_parentesco]["cumple"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    fecha_formateada = f"{fecha_cumple.year}-{fecha_cumple.month}-{fecha_cumple.day}"

                    cursor.execute(sql_insert_cn_parentesco_con_cumple,
                               (
                                   fk_cliente_inserted,
                                   parentesco[index_parentesco]["tipo_parentesco"],
                                   parentesco[index_parentesco]["sexo"],
                                   parentesco[index_parentesco]["nombre1"],
                                   parentesco[index_parentesco]["nombre2"],
                                   parentesco[index_parentesco]["apellido1"],
                                   parentesco[index_parentesco]["apellido2"],
                                   parentesco[index_parentesco]["celular"],
                                   parentesco[index_parentesco]["correo"],
                                   fecha_formateada
                               )
                               )                
                
                connection.commit()
                fk_cliente_parentesco_inserted = cursor.lastrowid
                ids_parentesco.append(fk_cliente_parentesco_inserted)

            else:
                if not parentesco[index_parentesco]["cumple"]:
                    # Debo de usar sin cumple
                    cursor.execute(sql_update_cn_parentesco_sin_cumple,
                               (
                                   parentesco[index_parentesco]["tipo_parentesco"],
                                   parentesco[index_parentesco]["sexo"],
                                   parentesco[index_parentesco]["nombre1"],
                                   parentesco[index_parentesco]["nombre2"],
                                   parentesco[index_parentesco]["apellido1"],
                                   parentesco[index_parentesco]["apellido2"],
                                   parentesco[index_parentesco]["celular"],
                                   parentesco[index_parentesco]["correo"],
                                   parentesco[index_parentesco]["id"],
                                   fecha_formateada
                               )
                               )
                else:
                    # Debo de usar con cumple
                    fecha_cumple = datetime.datetime.strptime(parentesco[index_parentesco]["cumple"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    fecha_formateada = f"{fecha_cumple.year}-{fecha_cumple.month}-{fecha_cumple.day}"
                    cursor.execute(sql_update_cn_parentesco_con_cumple,
                               (
                                   parentesco[index_parentesco]["tipo_parentesco"],
                                   parentesco[index_parentesco]["sexo"],
                                   parentesco[index_parentesco]["nombre1"],
                                   parentesco[index_parentesco]["nombre2"],
                                   parentesco[index_parentesco]["apellido1"],
                                   parentesco[index_parentesco]["apellido2"],
                                   parentesco[index_parentesco]["celular"],
                                   parentesco[index_parentesco]["correo"],
                                   parentesco[index_parentesco]["cumple"],
                                   parentesco[index_parentesco]["id"],
                                   fecha_formateada
                               )
                               )
                                    
                connection.commit()

                ids_parentesco.append(parentesco[index_parentesco]["id"])

        if ids_parentesco:
            converted_list = [str(element) for element in ids_parentesco]
            string_busqueda_ids = ",".join(converted_list)
            sql_ids_parentescos_x_remover = """
                                                SELECT
                                                parentesco.id
                                                FROM parentesco
                                                WHERE parentesco.fk_cliente = %s
                                                AND parentesco.publish = TRUE
                                            """

            cursor.execute(sql_ids_parentescos_x_remover, (fk_cliente_inserted,))
            rows = [item['id'] for item in cursor.fetchall()]

            sql_eliminar_parentescos = """
                                        UPDATE parentesco
                                        SET publish = FALSE
                                        WHERE fk_cliente = %s
                                        AND id = %s
                                        AND publish = TRUE
                                        """

            temp3 = list(set(rows) - set(ids_parentesco))

            for row in temp3:
                if row:
                    cursor.execute(sql_eliminar_parentescos, (fk_cliente_inserted, row))
                    connection.commit()

        # ------------------------------------->FIN PARENTESCO<-------------------------------------------------------
