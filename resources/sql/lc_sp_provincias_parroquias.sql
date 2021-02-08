DROP PROCEDURE IF EXISTS `lc_sp_provincias_parroquias`;
DELIMITER $$
CREATE PROCEDURE lc_sp_provincias_parroquias(
    IN pProvinciaParroquia JSON,
    OUT records_affected JSON
)

BEGIN
    DECLARE vJsonEsValido INT;
    DECLARE vJsonSalida json;
    DECLARE vItems INT;
    DECLARE vIndex BIGINT UNSIGNED DEFAULT 0;
    

    SET vJsonEsValido = JSON_VALID(pProvinciaParroquia);
    SET records_affected = '{}';

     IF vJsonEsValido = 0 THEN 
        # El objeto JSON no es válido, salimos prematuramente
        SELECT "JSON suministrado no es válido";
    ELSE 
        SET vItems = JSON_LENGTH(pProvinciaParroquia);

        IF vItems > 0 THEN 
            WHILE vIndex < vItems DO
                    # SELECT JSON_UNQUOTE(JSON_EXTRACT(pProvinciaParroquia, CONCAT('$."',vIndex+1,'"'))) as Result;   
                    SET vJsonSalida =   JSON_EXTRACT(pProvinciaParroquia,CONCAT('$[', vIndex, ']'));           
                    SET records_affected =  JSON_ARRAY_APPEND(records_affected,'$',  JSON_EXTRACT(pProvinciaParroquia,CONCAT('$[', vIndex, ']')));

            SET vIndex = vIndex + 1;
            END WHILE;

        END IF;
    END IF;

END
$$

DELIMITER;