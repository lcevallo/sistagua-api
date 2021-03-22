CREATE VIEW v_info_cliente_empresarial
AS
SELECT
  `sistagua_bd`.`cliente_empresarial`.`id` AS `id`,
  `sistagua_bd`.`cliente_empresarial`.`codigo` AS `codigo`,
  `sistagua_bd`.`cliente_empresarial`.`ruc` AS `ruc`,
  `sistagua_bd`.`cliente_empresarial`.`nombres` AS `nombre_empresa`,
  `sistagua_bd`.`cliente_empresarial`.`direccion` AS `direccion`,
  `sistagua_bd`.`cliente_empresarial`.`telefono` AS `telefono`,
  `sistagua_bd`.`cliente_empresarial`.`correo` AS `correo_empresa`,
  `sistagua_bd`.`cargo`.`nombres` AS `nombres`,
  `sistagua_bd`.`cargo`.`apellidos` AS `apellidos`,
  `sistagua_bd`.`tipo_cargo`.`tipo` AS `tipo`,
  `sistagua_bd`.`cargo`.`celular` AS `celular`,
  `sistagua_bd`.`cargo`.`cumple` AS `cumple`,
  `sistagua_bd`.`cargo`.`correo` AS `correo_cargo`,
  `sistagua_bd`.`tbl_provincia`.`provincia` AS `provincia`,
  `sistagua_bd`.`tbl_canton`.`canton` AS `canton`,
  `sistagua_bd`.`tbl_parroquia`.`parroquia` AS `parroquia`,
  `sistagua_bd`.`oficinas_empresa`.`sector` AS `sector`,
  `sistagua_bd`.`oficinas_empresa`.`direccion` AS `direccion_cargo`,
  `sistagua_bd`.`oficinas_empresa`.`telefono_convencional` AS `telefono_convencional`,
  `sistagua_bd`.`cliente_empresarial`.`publish` AS `publish`
FROM
  `contactos_empresa`
  RIGHT OUTER JOIN `cliente_empresarial` ON (`contactos_empresa`.`fk_cliente_empresarial` = `cliente_empresarial`.`id`)
  LEFT OUTER JOIN `cargo` ON (`contactos_empresa`.`fk_cargo` = `cargo`.`id`)
  LEFT OUTER JOIN `oficinas_empresa` ON (`cliente_empresarial`.`id` = `oficinas_empresa`.`fk_cliente_empresarial`)
  LEFT OUTER JOIN `tbl_provincia` ON (`oficinas_empresa`.`fk_provincia` = `tbl_provincia`.`id`)
  LEFT OUTER JOIN `tbl_canton` ON (`tbl_provincia`.`id` = `tbl_canton`.`id_provincia`)
  AND (`oficinas_empresa`.`fk_canton` = `tbl_canton`.`id`)
  LEFT OUTER JOIN `tbl_parroquia` ON (`tbl_canton`.`id` = `tbl_parroquia`.`id_canton`)
  AND (`oficinas_empresa`.`fk_parroquia` = `tbl_parroquia`.`id`)
  LEFT OUTER JOIN `tipo_cargo` ON (`cargo`.`fk_tipo_cargo` = `tipo_cargo`.`id`)