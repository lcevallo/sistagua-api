DROP PROCEDURE IF EXISTS `lc_sp_eliminar_cliente_natural`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lc_sp_eliminar_cliente_natural`(
    IN pClienteNaturalId BIGINT(11),
    OUT outSalida JSON
)
BEGIN


    UPDATE direccion_cliente
    SET publish = FALSE
    WHERE fk_cliente = pClienteNaturalId;


    UPDATE parentesco
    SET publish = FALSE
    WHERE fk_cliente = pClienteNaturalId;

    UPDATE cliente_natural
    SET publish = FALSE
    WHERE id = pClienteNaturalId;


    SET outSalida = SELECT JSON_OBJECT('id_cliente',id)   FROM cliente_natural WHERE id = pClienteNaturalId;
    UNION
    SELECT JSON_OBJECT('id_parentesco',id) FROM parentesco WHERE fk_cliente = pClienteNaturalId
    UNION
    SELECT JSON_OBJECT('id_direccion',id) FROM direccion_cliente WHERE fk_cliente = pClienteNaturalId;

END;