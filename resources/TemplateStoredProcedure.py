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

        ids_parentesco = []
        for index_parentesco in range(parentesco_size):

            if not parentesco[index_parentesco]["id"]:
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
                                   parentesco[index_parentesco]["cumple"]
                               )
                               )

                fk_cliente_parentesco_inserted = cursor.lastrowid
                ids_parentesco.append(fk_cliente_parentesco_inserted)

            else:

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
                                   fk_cliente_inserted,
                               )
                               )

                if cursor.rowcount > 0:
                    ids_parentesco.append(parentesco[index_parentesco]["id"])

        str1 = " "
        string_busqueda_ids = str1.join(ids_parentesco)
        sql_ids_parentescos_x_remover = """
                                            SELECT
                                            parentesco.id
                                            FROM parentesco
                                            WHERE parentesco.fk_cliente NOT IN (%s)
                                            AND parentesco.publish = TRUE
                                        """

        cursor.execute(sql_ids_parentescos_x_remover, (string_busqueda_ids,))
        rows = cursor.fetchall()

        sql_eliminar_parentescos = """
                                    UPDATE parentesco
                                    SET publish = FALSE
                                    WHERE fk_cliente = ?
                                    AND id = ?
                                    AND publish = TRUE
                                    """

        for row in rows:
            if row:
                cursor.execute(sql_eliminar_parentescos, (fk_cliente_inserted, row))

        # ------------------------------------->FIN PARENTESCO<-------------------------------------------------------
