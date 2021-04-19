-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 16-04-2021 a las 14:04:24
-- Versión del servidor: 10.3.28-MariaDB
-- Versión de PHP: 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistagua_bd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica`
--

DROP TABLE `ficha_tecnica_detalle_accesorio`;
DROP TABLE `ficha_tecnica_detalle_filtracion`;
DROP TABLE `ficha_tecnica_detalle`;
DROP TABLE `ficha_tecnica`;




CREATE TABLE `hoja_control` (
  `id` int(11) NOT NULL,
  `fk_cliente` int(11) DEFAULT NULL,
  `tipo_cliente` int(11) DEFAULT NULL,
  `codigo` int(11) DEFAULT NULL,
  `tds` int(11) DEFAULT NULL,
  `ppm` int(11) DEFAULT NULL,
  `visitas` int(11) DEFAULT NULL,
  `fecha_comprado` date DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla donde guardare la hoja de control';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle`
--

CREATE TABLE `hoja_control_detalle` (
  `id` int(11) NOT NULL,
  `fk_hoja_control` int(11) DEFAULT NULL,
  `factura` varchar(255) DEFAULT NULL,
  `fecha_mantenimiento` date DEFAULT NULL,
  `recibo` varchar(255) DEFAULT NULL,
  `hoja_control` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `persona_autoriza` varchar(255) DEFAULT NULL,
  `firma_url` varchar(255) DEFAULT NULL,
  `cedula_autoriza` varchar(10) DEFAULT NULL,
  `persona_dio_mantenimiento` varchar(255) DEFAULT NULL,
  `cedula_dio_mantenimiento` varchar(10) DEFAULT NULL,
  `ppm` int(11) DEFAULT NULL,
  `tds` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
   PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla detalle de hoja de control';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle_accesorio`
--

CREATE TABLE `hoja_control_detalle_accesorio` (
  `id` int(11) NOT NULL,
  `fk_hoja_control_detalle` int(11) DEFAULT NULL,
  `fk_accesorio` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla que guardara los accesorios que se entregaran en la Hoja de control detalle ';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle_filtracion`
--

CREATE TABLE `hoja_control_detalle_filtracion` (
  `id` int(11) NOT NULL,
  `fk_hoja_control_detalle` int(11) DEFAULT NULL,
  `fk_filtracion` int(11) DEFAULT NULL,
  `valor_filtracion` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla que guardara el detalle de Hoja de Control detalle contra las filtraciones';


