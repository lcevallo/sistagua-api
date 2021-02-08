DROP PROCEDURE IF EXISTS `lc_sp_actualizar_ficha_tecnica`;
DELIMITER $$
CREATE PROCEDURE lc_sp_actualizar_ficha_tecnica(
    IN _id_FichaTecnica int,
    IN cedula VARCHAR(10),
    IN pFichaTecnica JSON,
    OUT records_affected INT
)
BEGIN
    DECLARE vJsonEsValido INT;
    DECLARE vItems INT;
    DECLARE vIndex BIGINT UNSIGNED DEFAULT 0;
    DECLARE countRow INT;

    # Variables para parseo del objeto JSON
    DECLARE vFk_cliente int(11);
    DECLARE vCodigo int(11);
    DECLARE vTds int(11);
    DECLARE vPpm int(11);
    DECLARE vVisitas int(11);
    DECLARE vFecha_comprado date;


    SET vJsonEsValido = JSON_VALID(pFichaTecnica);
    IF vJsonEsValido = 0 THEN 
                # El objeto JSON no es válido, salimos prematuramente
                SELECT "JSON suministrado no es válido";
                
    ELSE
                    # Nuestro objeto es válido, podemos proceder
                    SET vItems = JSON_LENGTH(pFichaTecnica);
                    # El objeto es válido y contiene al menos un elemento
                    IF vItems > 0 THEN 
        
                    SELECT
                    cliente_ficha.id INTO vFk_cliente
                    FROM cliente_ficha
                    WHERE cliente_ficha.cedula = cliente_ficha.cedula;

                        WHILE vIndex < vItems DO
        
                            SET vFk_cliente=  JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].fk_cliente'));
                            SET vCodigo=  JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].codigo'));
                            SET vTds=  JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].tds'));
                            SET vPpm=  JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].ppm'));
                            SET vVisitas=  JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].visitas'));
                            SET vFecha_comprado=  JSON_UNQUOTE(JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, '].fecha_comprado')));
                            
                            UPDATE ficha_tecnica
                            SET 
                                fk_cliente = vFk_cliente,
                                codigo = vCodigo,
                                tds = vTds,
                                ppm = vPpm,
                                visitas = vVisitas,
                                fecha_comprado = vFecha_comprado,
                                updated_at = CURRENT_TIMESTAMP()
                            WHERE publish = TRUE
                            AND id = _id_FichaTecnica;

                            SET countRow =  ROW_COUNT();
        
                            IF countRow > 0 THEN
                                SET records_affected = countRow;
                            ELSE
                                SET records_affected = -1;
                            END IF;
                            SET vIndex = vIndex + 1;
                        END WHILE;
                        
                    END IF;
            END IF;
END

$$

DELIMITER;