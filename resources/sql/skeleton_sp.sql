DROP PROCEDURE IF EXISTS `lc_sp_skeleton`;
DELIMITER $$
CREATE DEFINER = 'sistagua'@'localhost' PROCEDURE lc_sp_skeleton(
    IN pProvinciaParroquia JSON,
    OUT records_affected INT
)

BEGIN
    DECLARE vJsonEsValido INT;
    DECLARE vItems INT;
    DECLARE vIndex BIGINT UNSIGNED DEFAULT 0;

    SET vJsonEsValido = JSON_VALID(pProvinciaParroquia);

     IF vJsonEsValido = 0 THEN 
        # El objeto JSON no es válido, salimos prematuramente
        SELECT "JSON suministrado no es válido";
    ELSE 
        SET vItems = JSON_LENGTH(pProvinciaParroquia);

        IF vItems > 0 THEN 
            WHILE vIndex < vItems DO





            SET vIndex = vIndex + 1;
            END WHILE;

        END IF;
    END IF;

END
$$

DELIMITER;