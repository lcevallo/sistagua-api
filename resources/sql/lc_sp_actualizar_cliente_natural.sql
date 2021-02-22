DROP PROCEDURE IF EXISTS `lc_sp_actualizar_cliente_natural`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lc_sp_actualizar_cliente_natural`(
    IN pClienteNatural JSON,
    IN pParentescos JSON,
    IN pDirecciones JSON,
    OUT outSalida JSON

)
BEGIN

    DECLARE vJsonEsValidoCliente INT;
    DECLARE vJsonEsValidoParentesco INT;
    DECLARE vJsonEsValidoDirecciones INT;
    DECLARE vItemsCliente INT;
    DECLARE vItemsParentesco INT;
    DECLARE vItemsDirecciones INT;
    DECLARE vIndexCliente BIGINT UNSIGNED DEFAULT 0;
    DECLARE vIndexParentesco BIGINT UNSIGNED DEFAULT 0;
    DECLARE vIndexDirecciones BIGINT UNSIGNED DEFAULT 0;
    DECLARE vCumpleParentesco VARCHAR(60);


    DECLARE vfk_cliente BIGINT(11);
    DECLARE vid_parentesco BIGINT(11);
    DECLARE vid_direccion BIGINT(11);
    DECLARE cliente_natural_rows int;


    SET vJsonEsValidoCliente = JSON_VALID(pClienteNatural);
    SET vJsonEsValidoParentesco = JSON_VALID(pParentescos);
    SET vJsonEsValidoDirecciones = JSON_VALID(pDirecciones);


    SET outSalida = '[{"id_cliente":[]},{"id_parentesco":[]},{"id_direcciones":[]}]';




    IF vJsonEsValidoCliente = 0 AND vJsonEsValidoParentesco = 0 AND vJsonEsValidoDirecciones = 0  THEN
        # El objeto JSON no es válido, salimos prematuramente
        SELECT "JSON suministrado no es válido";
    ELSE
        # Primero Cliente Natural debe devolver el id
        SET vItemsCliente = JSON_LENGTH(pClienteNatural);

        # El objeto es válido y contiene al menos un elemento
            IF vItemsCliente > 0 THEN
                WHILE vIndexCliente < vItemsCliente DO

                    SET vCumpleParentesco = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].cumple')));

                    IF trim(coalesce(vCumpleParentesco, '')) <>''  THEN
                        SET vCumpleParentesco = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].cumple')));
                    ELSE
                        SET vCumpleParentesco = null;
                    END IF;


                    SET vfk_cliente = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].id')));


                    #Aqui debo de actualizar
                    IF EXISTS(Select 1 from cliente_natural where publish=true AND id= vfk_cliente) THEN

                        UPDATE cliente_natural
                        SET codigo = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].codigo'))),
                            ruc = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].ruc'))),
                            nombre1 = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].nombre1'))),
                            nombre2 = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].nombre2'))),
                            apellido1 = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].apellido1'))),
                            apellido2 = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].apellido2'))),
                            correo = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].correo'))),
                            celular = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].celular'))),
                            cumple = vCumpleParentesco,
                            foto = JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].foto')))
                        WHERE id = vfk_cliente
                        AND publish = TRUE;

                        -- SELECT ROW_COUNT() into cliente_natural_rows;

                        -- SELECT JSON_ARRAY_INSERT(outSalida, '$[0].id_cliente[0]', vfk_cliente);
                        SET outSalida= JSON_ARRAY_INSERT(outSalida, '$[0].id_cliente[0]', vfk_cliente);

                    #Aqui debo de insertar
                    ELSE
                        INSERT INTO cliente_natural (
                                codigo,
                                ruc,
                                nombre1,
                                nombre2,
                                apellido1,
                                apellido2,
                                correo,
                                celular,
                                cumple,
                                foto)
                        VALUES (
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].codigo'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].ruc'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].nombre1'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].nombre2'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].apellido1'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].apellido2'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].correo'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].celular'))),
                                -- JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].cumple'))),
                                vCumpleParentesco,
                                JSON_UNQUOTE(JSON_EXTRACT(pClienteNatural, CONCAT('$[', vIndexCliente, '].foto')))
                                );
                        SET vfk_cliente = LAST_INSERT_ID();
                        -- SELECT ROW_COUNT() into cliente_natural_rows;

                        SET outSalida= JSON_ARRAY_INSERT(outSalida, '$[0].id_cliente[0]', LAST_INSERT_ID());

                    END IF;

                    SET vIndexCliente = vIndexCliente + 1;
                END WHILE;
            END IF;

        # Segundo Voy por el parentesco
        SET vItemsParentesco = JSON_LENGTH(pParentescos);

        # El objeto es válido y contiene al menos un elemento
            IF vItemsParentesco > 0 THEN

                WHILE vIndexParentesco < vItemsParentesco DO

                    SET vCumpleParentesco = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].cumple')));

                    IF trim(coalesce(vCumpleParentesco, '')) <>''  THEN
                        SET vCumpleParentesco = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].cumple')));
                    ELSE
                        SET vCumpleParentesco = null;
                    END IF;


                    IF JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].id')) IS NULL THEN
                         SET vid_parentesco= null;
                    END IF;

                    SET vid_parentesco=JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].id')));

                    IF EXISTS(Select 1 from parentesco where publish=true AND fk_cliente=vfk_cliente AND id= vid_parentesco) THEN

                        UPDATE parentesco
                        SET tipo_parentesco = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].tipo_parentesco'))),
                            sexo = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].sexo'))),
                            nombre1 = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].nombre1'))),
                            nombre2 = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].nombre2'))),
                            apellido1 = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].apellido1'))),
                            apellido2 =JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].apellido2'))),
                            celular = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].celular'))),
                            correo = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].correo'))),
                            cumple = vCumpleParentesco
                        WHERE id = vid_parentesco
                        AND fk_cliente = vfk_cliente;
                        -- AND fk_cliente = JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].fk_cliente')));


                        -- SET outSalida = JSON_SET(outSalida,CONCAT('$.id_parentesco',vIndexParentesco) , vid_parentesco);
                        -- SET outSalida = JSON_OBJECTAGG(outSalida,JSON_OBJECT('id_parentesco', vid_parentesco));

                        SET outSalida = JSON_ARRAY_INSERT(outSalida, CONCAT('$[1].id_parentesco[',vIndexParentesco,']'), vid_parentesco);

                    ELSE
                        INSERT INTO parentesco (
                            fk_cliente,
                            tipo_parentesco,
                            sexo,
                            nombre1,
                            nombre2,
                            apellido1,
                            apellido2,
                            celular,
                            correo,
                            cumple)
                        VALUES (
                            vfk_cliente,
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].tipo_parentesco'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].sexo'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].nombre1'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].nombre2'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].apellido1'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].apellido2'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].celular'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].correo'))),
                            -- JSON_UNQUOTE(JSON_EXTRACT(pParentescos, CONCAT('$[', vIndexParentesco, '].cumple')))
                            vCumpleParentesco
                            );

                          -- SET outSalida = JSON_SET(outSalida,CONCAT('$.id_parentesco',vIndexParentesco) , LAST_INSERT_ID());
                        --   SET outSalida = JSON_OBJECTAGG(outSalida,JSON_OBJECT('id_parentesco', LAST_INSERT_ID()));
                        --   SELECT JSON_ARRAY_INSERT(outSalida, CONCAT('$[1].id_parentesco[',vIndexParentesco,']'), LAST_INSERT_ID());
                          SET outSalida= JSON_ARRAY_INSERT(outSalida, CONCAT('$[1].id_parentesco[',vIndexParentesco,']'), LAST_INSERT_ID());

                    END IF;

                    SET vIndexParentesco = vIndexParentesco + 1;
                END WHILE;
            END IF;

        #Tercero agregar las direcciones del cliente
        SET vItemsDirecciones = JSON_LENGTH(pDirecciones);

        # El objeto es válido y contiene al menos un elemento
            IF vItemsDirecciones > 0 THEN

                WHILE vIndexDirecciones < vItemsDirecciones DO
                    SET vid_direccion=JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].id')));

                    IF EXISTS(Select 1 from direccion_cliente where publish=true AND fk_cliente=vfk_cliente AND id= vid_direccion) THEN

                        UPDATE direccion_cliente
                        SET fk_provincia = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_provincia'))),
                            fk_canton = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_canton'))),
                            fk_parroquia = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_parroquia'))),
                            direccion_domiciliaria = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_domiciliaria'))),
                            direccion_oficina = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_oficina'))),
                            telefono_convencional = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].telefono_convencional')))
                        WHERE
                        -- fk_cliente = JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_cliente')))
                        fk_cliente = vfk_cliente
                        AND id = vid_direccion;


                        -- SET outSalida = JSON_SET(outSalida,CONCAT('$.id_direccion',vIndexDirecciones) , vid_direccion);
                        -- SELECT JSON_ARRAY_INSERT(outSalida, CONCAT('$[2].id_direcciones[',vIndexDirecciones,']'), vid_direccion);
                        SET outSalida=JSON_ARRAY_INSERT(outSalida, CONCAT('$[2].id_direcciones[',vIndexDirecciones,']'), vid_direccion);

                    ELSE

                        INSERT INTO direccion_cliente (
                            fk_cliente,
                            fk_provincia,
                            fk_canton,
                            fk_parroquia,
                            direccion_domiciliaria,
                            direccion_oficina,
                            telefono_convencional
                            )
                        VALUES (
                            vfk_cliente,
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_provincia'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_canton'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_parroquia'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_domiciliaria'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_oficina'))),
                            JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].telefono_convencional')))
                            );


                            -- SET outSalida = JSON_SET(outSalida,CONCAT('$.id_direccion',vIndexDirecciones), LAST_INSERT_ID());
                            -- SELECT JSON_ARRAY_INSERT(outSalida, CONCAT('$[2].id_direcciones[',vIndexDirecciones,']'), LAST_INSERT_ID());
                            SET outSalida= JSON_ARRAY_INSERT(outSalida, CONCAT('$[2].id_direcciones[',vIndexDirecciones,']'), LAST_INSERT_ID());

                    END IF;

                    SET vIndexDirecciones = vIndexDirecciones + 1;
                END WHILE;

            END IF;


    END IF;


END$$
DELIMITER ;