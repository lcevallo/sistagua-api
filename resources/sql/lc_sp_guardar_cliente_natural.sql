DELIMITER $$

CREATE DEFINER = 'sistagua'@'localhost' PROCEDURE lc_sp_guardar_cliente_natural(
    IN pClienteNatural JSON,
    IN pParentescos JSON,
    IN pDirecciones JSON,
    OUT pIdCliente BIGINT(11)

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


    DECLARE last_inserted_cliente_natural_id BIGINT(11);


    SET vJsonEsValidoCliente = JSON_VALID(pClienteNatural);
    SET vJsonEsValidoParentesco = JSON_VALID(pParentescos);
    SET vJsonEsValidoDirecciones = JSON_VALID(pDirecciones);

    
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
                    
                    SET last_inserted_cliente_natural_id = LAST_INSERT_ID();

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
                            last_inserted_cliente_natural_id, 
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

                    SET vIndexParentesco = vIndexParentesco + 1;
                END WHILE;
            END IF;

        #Tercero agregar las direcciones del cliente
        SET vItemsDirecciones = JSON_LENGTH(pDirecciones);

        # El objeto es válido y contiene al menos un elemento
            IF vItemsDirecciones > 0 THEN

                WHILE vIndexDirecciones < vItemsDirecciones DO

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
                                last_inserted_cliente_natural_id,
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_provincia'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_canton'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].fk_parroquia'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_domiciliaria'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].direccion_oficina'))),
                                JSON_UNQUOTE(JSON_EXTRACT(pDirecciones, CONCAT('$[', vIndexDirecciones, '].telefono_convencional')))
                                );

                    SET vIndexDirecciones = vIndexDirecciones + 1;
                END WHILE;
            END IF;

        Set pIdCliente = last_inserted_cliente_natural_id;
    END IF;    
    
    -- INSERT INTO cliente_natural (codigo, ruc, nombre1, nombre2, apellido1, apellido2, correo, celular, cumple, foto)
    -- VALUES (?, ?, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)

    -- INSERT INTO parentesco (fk_cliente, tipo_parentesco, sexo, nombre1, nombre2, apellido1, apellido2, celular, correo, cumple)
    -- VALUES (?, ?, ?, ?, ?, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)

    -- INSERT INTO direccion_cliente (fk_cliente, fk_provincia, fk_canton, fk_parroquia, direccion_domiciliaria, direccion_oficina, telefono_convencional)
    -- VALUES (?, ?, ?, ?, DEFAULT, DEFAULT, DEFAULT)  


END

$$
DELIMITER;