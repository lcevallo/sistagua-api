

DROP PROCEDURE IF EXISTS `lc_spGuardarFichaTecnica`;
DELIMITER $$
CREATE DEFINER = 'sistagua'@'localhost'
CREATE PROCEDURE lc_spGuardarFichaTecnica(
    _id_FichaTecnica int,
    IN pDetallesJson JSON,
    OUT pJson_ids TEXT
)
BEGIN
    DECLARE vJsonEsValido INT;
    DECLARE vItems INT;
    DECLARE vIndex BIGINT UNSIGNED DEFAULT 0;

    # Variables para parseo del objeto JSON
        DECLARE last_inserted_ficha_tecnica_detalle_id BIGINT(11);   
        DECLARE vFk_ficha_tecnica INT;
        DECLARE vFactura VARCHAR(255);
        DECLARE vFecha_mantenimiento DATE;
        DECLARE vRecibo VARCHAR(255);
        DECLARE vFicha_tecnica VARCHAR(255);
        DECLARE vDescripcion TEXT;
        DECLARE vPersona_recepta VARCHAR(255);
        DECLARE vFirma_url VARCHAR(255);
        DECLARE vCedula_receptor VARCHAR(10);
        DECLARE vPersona_dio_mantenimiento VARCHAR(255);
        DECLARE vCedula_dio_mantenimiento VARCHAR(10);
        DECLARE vCreated_at DATETIME;
        DECLARE vUpdated_at DATETIME;
        DECLARE vPublish TINYINT;

        SET vJsonEsValido = JSON_VALID(pDetallesJson);
        SET pJson_ids = '[';

        IF EXISTS (SELECT 1 FROM `ficha_tecnica` where `ficha_tecnica`.`id` = _id_FichaTecnica  AND `ficha_tecnica`.`publish` = true) THEN

            IF vJsonEsValido = 0 THEN 
                # El objeto JSON no es válido, salimos prematuramente
                SELECT "JSON suministrado no es válido";
                SET pJson_ids = '0';
            ELSE
                    # Nuestro objeto es válido, podemos proceder
                    SET vItems = JSON_LENGTH(pDetallesJson);
                    # El objeto es válido y contiene al menos un elemento
                    IF vItems > 0 THEN 
        
                        WHILE vIndex < vItems DO
        
                            SET vFactura=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].factura')));
                            SET vFecha_mantenimiento=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].fecha_mantenimiento')));
                            SET vRecibo=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].recibo')));
                            SET vFicha_tecnica=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].ficha_tecnica')));
                            SET vDescripcion=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].descripcion')));
                            SET vPersona_recepta=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].persona_recepta')));
                            SET vFirma_url=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].firma_url')));
                            SET vCedula_receptor=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].cedula_receptor')));
                            SET vPersona_dio_mantenimiento=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].persona_dio_mantenimiento')));
                            SET vCedula_dio_mantenimiento=  JSON_UNQUOTE(JSON_EXTRACT(pDetallesJson, CONCAT('$[', vIndex, '].cedula_dio_mantenimiento')));
        
                            INSERT INTO ficha_tecnica_detalle (fk_ficha_tecnica, factura, fecha_mantenimiento, recibo, ficha_tecnica, descripcion, persona_recepta, firma_url, cedula_receptor, persona_dio_mantenimiento, cedula_dio_mantenimiento)
                            VALUES (_id_FichaTecnica, vFactura, vFecha_mantenimiento, vRecibo, vFicha_tecnica, vDescripcion, vPersona_recepta, vFirma_url, vCedula_receptor, vPersona_dio_mantenimiento, vCedula_dio_mantenimiento);
                            SET last_inserted_ficha_tecnica_detalle_id = LAST_INSERT_ID();
        
                            -- SET pJson_ids = JSON_ARRAY_APPEND(pJson_ids, '$', CONCAT('{"id":', last_inserted_ficha_tecnica_detalle_id,','));
                            IF vIndex = 0 THEN    
                                SET pJson_ids = CONCAT(pJson_ids,'',last_inserted_ficha_tecnica_detalle_id);
                            ELSE
                                SET pJson_ids = CONCAT(pJson_ids,',',last_inserted_ficha_tecnica_detalle_id);
                            END IF;
                            SET vIndex = vIndex + 1;
                        END WHILE;
                        SET pJson_ids = CONCAT(pJson_ids,']');
                    END IF;
            END IF;
        ELSE
            SET pJson_ids = '-1';
        END IF;
END
$$
DELIMITER;