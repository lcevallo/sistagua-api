DROP PROCEDURE IF EXISTS `lc_sp_get_table_cliente_natural`;
DELIMITER $$
CREATE  DEFINER = 'sistagua'@'localhost' PROCEDURE lc_sp_get_table_cliente_natural(
    IN pIdCliente BIGINT,
    OUT jsonRecordsCliente JSON,
    OUT jsonRecordsDirecciones JSON,
    OUT jsonRecordsParentesco JSON
)

BEGIN
    
    SELECT JSON_ARRAYAGG(JSON_OBJECT('id',id, 'codigo',codigo, 'ruc',ruc, 'nombre1',nombre1, 'nombre2',nombre2, 'apellido1',apellido1, 'apellido2',apellido2, 'correo',correo, 'celular',celular, 'cumple',cumple, 'foto',foto, 'publish',publish)) into jsonRecordsCliente from cliente_natural where id = pIdCliente;
    SELECT JSON_ARRAYAGG(JSON_OBJECT('id',id, 'fk_cliente',fk_cliente, 'tipo_parentesco',tipo_parentesco, 'sexo',sexo, 'nombre1',nombre1, 'nombre2',nombre2, 'apellido1',apellido1, 'apellido2',apellido2, 'celular',celular, 'correo',correo, 'cumple',cumple)) into jsonRecordsParentesco from parentesco where fk_cliente=pIdCliente;
    SELECT JSON_ARRAYAGG(JSON_OBJECT('id',id, 'fk_cliente',fk_cliente, 'fk_provincia',fk_provincia, 'fk_canton',fk_canton, 'fk_parroquia',fk_parroquia, 'direccion_domiciliaria',direccion_domiciliaria, 'direccion_oficina',direccion_oficina, 'telefono_convencional',telefono_convencional, 'publish',publish)) into jsonRecordsDirecciones from direccion_cliente where fk_cliente=pIdCliente;
END
$$

DELIMITER;