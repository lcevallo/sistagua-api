-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 02-02-2021 a las 10:25:25
-- Versión del servidor: 10.3.27-MariaDB
-- Versión de PHP: 7.3.6

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
CREATE DATABASE IF NOT EXISTS `sistagua_bd` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sistagua_bd`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accesorios`
--

CREATE TABLE `accesorios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `created_at` varchar(255) DEFAULT NULL,
  `updated_at` varchar(255) DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla se guarda los accesorios que se van a vender';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id`, `nombre`, `estado`, `created_at`) VALUES
(1, 'Filtración', 1, '2020-07-20 12:56:41'),
(2, 'Accesorios', 1, '2020-07-25 11:56:06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciudad`
--

CREATE TABLE `ciudad` (
  `id` int(11) NOT NULL,
  `provincia_id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ciudad`
--

INSERT INTO `ciudad` (`id`, `provincia_id`, `nombre`, `estado`) VALUES
(1, 1, 'Cuenca', 1),
(2, 1, 'Girón', 1),
(3, 1, 'Gualaceo', 1),
(4, 1, 'Nabón', 1),
(5, 1, 'Paute', 1),
(6, 1, 'Pucara', 1),
(7, 1, 'San Fernando', 1),
(8, 1, 'Santa Isabel', 1),
(9, 1, 'Sigsig', 1),
(10, 1, 'Oña', 1),
(11, 1, 'Chordeleg', 1),
(12, 1, 'El Pan', 1),
(13, 1, 'Sevilla de Oro', 1),
(14, 1, 'Guachapala', 1),
(15, 1, 'Camilo Ponce Enríquez', 1),
(16, 2, 'Guaranda', 1),
(17, 2, 'Chillanes', 1),
(18, 2, 'Chimbo', 1),
(19, 2, 'Echendía', 1),
(20, 2, 'San Miguel', 1),
(21, 2, 'Caluma', 1),
(22, 2, 'Las Naves', 1),
(23, 3, 'Azogues', 1),
(24, 3, 'Biblían', 1),
(25, 3, 'Cañar', 1),
(26, 3, 'La Troncal', 1),
(27, 3, 'El Tambo', 1),
(28, 3, 'Déleg', 1),
(29, 3, 'Suscal', 1),
(30, 4, 'Tulcán', 1),
(31, 4, 'Bolívar', 1),
(32, 4, 'Espejo', 1),
(33, 4, 'Mira', 1),
(34, 4, 'Montúfar', 1),
(35, 4, 'San Pedro de Huaca', 1),
(36, 5, 'Latacunga', 1),
(37, 5, 'La Maná', 1),
(38, 5, 'Pangua', 1),
(39, 5, 'Pujilí', 1),
(40, 5, 'Salcedo', 1),
(41, 5, 'Saquisilí', 1),
(42, 5, 'Sigchos', 1),
(43, 6, 'Riobamba', 1),
(44, 6, 'Alausí', 1),
(45, 6, 'Colta', 1),
(46, 6, 'Chambo', 1),
(47, 6, 'Chunchi', 1),
(48, 6, 'Guamote', 1),
(49, 6, 'Guano', 1),
(50, 6, 'Pallatanga', 1),
(51, 6, 'Penipe', 1),
(52, 6, 'Cumandá', 1),
(53, 7, 'Machala', 1),
(54, 7, 'Arenillas', 1),
(55, 7, 'Atahualpa', 1),
(56, 7, 'Balsas', 1),
(57, 7, 'Chilla', 1),
(58, 7, 'El Guabo', 1),
(59, 7, 'Huaquillas', 1),
(60, 7, 'Marcabelí', 1),
(61, 7, 'Pasaje', 1),
(62, 7, 'Piñas', 1),
(63, 7, 'Portovelo', 1),
(64, 7, 'Santa Rosa', 1),
(65, 7, 'Zaruma', 1),
(66, 7, 'Las Lajas', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id` int(11) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `cedula` varchar(50) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id`, `correo`, `nombre`, `apellidos`, `cedula`, `telefono`, `created_at`) VALUES
(1, 'ccerezo90@gmail.com', 'Carlos Luis', 'Cerezo Romero', '0705114775', '0994898148', '2020-07-23 01:17:08'),
(2, 'sistagua@hotmail.com', 'Vicente ', 'Medina', '0705181667', '0997653175', '2020-07-27 10:12:21'),
(3, 'ccerezor@ulvr.edu.ec', 'Luis', 'Romero', '0705114777', '0994898148', '2020-07-28 22:25:52');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envio`
--

CREATE TABLE `envio` (
  `id` int(11) NOT NULL,
  `orden_id` int(11) NOT NULL,
  `ciudad_id` int(11) NOT NULL,
  `direccion` varchar(150) NOT NULL,
  `numero` varchar(50) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `envio`
--

INSERT INTO `envio` (`id`, `orden_id`, `ciudad_id`, `direccion`, `numero`, `referencia`, `created_at`) VALUES
(1, 24, 53, 'Ciudadela el maestro ', '0997653175', 'Laguna ', '2020-07-27 10:17:01'),
(2, 25, 2, 'Sauces 9', 'R22 v8', 'Diagonal al parque', '2020-07-27 21:29:12'),
(3, 26, 16, 'Sauces 9', 'R22 v8', 'Diagonal al parque', '2020-07-28 21:50:27'),
(4, 27, 16, 'Sauces 9', 'R22 v8', 'Diagonal al parque', '2020-07-28 22:20:23'),
(5, 28, 30, 'Alborada', 'r33 v2', 'diagonal al parque', '2020-07-28 22:24:47'),
(6, 29, 45, 'Alborada', 'r33 v2', 'diagonal al parque', '2020-07-28 22:26:21'),
(7, 30, 16, 'Sauces 9', 'R22 v8', 'Diagonal al parque', '2020-07-28 22:44:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica`
--

CREATE TABLE `ficha_tecnica` (
  `id` int(11) NOT NULL,
  `fk_cliente` int(11) DEFAULT NULL,
  `tds` int(11) DEFAULT NULL,
  `ppm` int(11) DEFAULT NULL,
  `visitas` int(11) DEFAULT NULL,
  `fecha_comprado` date DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla donde guardare la ficha tecnica';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle`
--

CREATE TABLE `ficha_tecnica_detalle` (
  `id` int(11) NOT NULL,
  `fk_ficha_tecnica` int(11) DEFAULT NULL,
  `factura` varchar(255) DEFAULT NULL,
  `fecha_mantenimiento` date DEFAULT NULL,
  `recibo` varchar(255) DEFAULT NULL,
  `ficha_tecnica` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `persona_recepta` varchar(255) DEFAULT NULL,
  `firma_url` varchar(255) DEFAULT NULL,
  `cedula_receptor` varchar(10) DEFAULT NULL,
  `persona_dio_mantenimiento` varchar(255) DEFAULT NULL,
  `cedula_dio_mantenimiento` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla detalle de ficha tecnica';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle_accesorio`
--

CREATE TABLE `ficha_tecnica_detalle_accesorio` (
  `id` int(11) NOT NULL,
  `fk_ficha_tecnica_detalle` int(11) DEFAULT NULL,
  `fk_accesorio` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla que guardara los accesorios que se entregaran en la ficha tecnica detalle ';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_tecnica_detalle_filtracion`
--

CREATE TABLE `ficha_tecnica_detalle_filtracion` (
  `id` int(11) NOT NULL,
  `fk_ficha_tecnica_detalle` int(11) DEFAULT NULL,
  `fk_filtracion` int(11) DEFAULT NULL,
  `valor_filtracion` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla que guardara el detalle de ficha tecnica detalle contra las filtraciones';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `filtracion`
--

CREATE TABLE `filtracion` (
  `id` int(11) NOT NULL,
  `filtracion` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `publish` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Es la tabla Filtraciones tendra diferentes valores';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden`
--

CREATE TABLE `orden` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `paid_amount` decimal(10,2) NOT NULL,
  `paid_amount_currency` varchar(10) NOT NULL,
  `txn_id` varchar(100) NOT NULL,
  `checkout_session_id` varchar(255) NOT NULL,
  `payment_status` varchar(25) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `orden`
--

INSERT INTO `orden` (`id`, `cliente_id`, `name`, `email`, `paid_amount`, `paid_amount_currency`, `txn_id`, `checkout_session_id`, `payment_status`, `created_at`) VALUES
(24, 2, NULL, 'sistagua@hotmail.com', 79.00, 'usd', 'pi_1H9Y1xLQkTCwQyreMcFaVcLo', 'cs_test_GdGaxQ6DVvvP0kgiEQbZeOZCevaCPjC901MPWMjqv8ywXFdOz9ZLlcnl', 'succeeded', '2020-07-27 10:17:01'),
(25, 1, NULL, 'ccerezo90@gmail.com', 271.15, 'usd', 'pi_1H9iYhLQkTCwQyreQoScnjKh', 'cs_test_ymL1jxI0t1o8uTxdoKVOOSl15xqpBCiHYi2UuKGXVbhXpEPR0nvgCH4M', 'succeeded', '2020-07-27 21:29:12'),
(26, 1, NULL, 'ccerezo90@gmail.com', 271.15, 'usd', 'pi_1HA5MmLQkTCwQyreb5jGbTPf', 'cs_test_BkKH3LDchTRIpolfp4W5Yemrb1asAHqBrcoPn2o5QtCaci7B7eTlfqn5', 'succeeded', '2020-07-28 21:50:27'),
(27, 1, NULL, 'ccerezo90@gmail.com', 271.15, 'usd', 'pi_1HA5pkLQkTCwQyreH44hkcbQ', 'cs_test_spScJt7rm17YlOF4gI9Hp6MjGhsXyZ3tV6iSRQmRUoEbkdrvHBmwSsbE', 'succeeded', '2020-07-28 22:20:23'),
(28, 1, NULL, 'ccerezo90@gmail.com', 271.15, 'usd', 'pi_1HA5tqLQkTCwQyreDxAcjil1', 'cs_test_jb3ibd5Lgea1bxK3PM2JwzaPq03ThVOQIIe01l1BGrWLIV7qylTCNbZ8', 'succeeded', '2020-07-28 22:24:47'),
(29, 3, NULL, 'ccerezo90@gmail.com', 79.00, 'usd', 'pi_1HA5vbLQkTCwQyrePUyNOe5Y', 'cs_test_hwXbbPcOQAZr8EFs0wHQZea2hNe7WPza8MhdEsJd7bYX6HmKj1GidGr7', 'succeeded', '2020-07-28 22:26:21'),
(30, 1, NULL, 'ccerezo90@gmail.com', 271.15, 'usd', 'pi_1HA6DNLQkTCwQyresOo9X1yt', 'cs_test_JUjXeWogQ0rrDZorllgiUcQydAnZxguvi7lxXbAh2b46yk0uPZgAAjQQ', 'succeeded', '2020-07-28 22:44:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_detalle`
--

CREATE TABLE `orden_detalle` (
  `id` int(11) NOT NULL,
  `orden_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `orden_detalle`
--

INSERT INTO `orden_detalle` (`id`, `orden_id`, `producto_id`, `precio`, `cantidad`) VALUES
(1, 24, 5, 75.00, 1.00),
(2, 25, 4, 267.15, 1.00),
(3, 26, 4, 267.15, 1.00),
(4, 27, 4, 267.15, 1.00),
(5, 28, 4, 267.15, 1.00),
(6, 29, 5, 75.00, 1.00),
(7, 30, 4, 267.15, 1.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `categoria_id` int(11) NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT 0.00,
  `foto` varchar(100) NOT NULL,
  `home` varchar(1) NOT NULL DEFAULT '0',
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `created_by` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `categoria_id`, `codigo`, `nombre`, `descripcion`, `precio`, `descuento`, `foto`, `home`, `fecha`, `estado`, `created_by`) VALUES
(3, 1, 'F-00001', 'ABLANDADOR AUTOMATICO', 'Ablandador en color azul', 1999.00, 0.00, 'images/productos/1e6c71a319042ecf28cab79e956ddd6a.jpg', '1', '2020-07-25 12:02:13', 'activo', 'admin'),
(4, 1, 'F-00002', 'ESTERELIZADOR UV 1GPM', 'Capacidad de Radiación: 30.000 micro watt seg/cm². Acero Inoxidable \r\nDiámetro 6.4 cm x Largo 34 cm \r\n', 267.15, 0.00, 'images/productos/4ede32fddf2b9f7b2ed0c70a08220e41.jpg', '1', '2020-07-25 12:05:50', 'activo', 'admin'),
(5, 1, 'F-00003', 'MENBRANA ÓSMOSIS INVERSA 75 GPD', 'Marca: FILMTEC - U.S.A\r\nSe utiliza en equipo de O.I. \r\nMod. CE-2/ CE-4/ CE-7\r\n', 75.00, 0.00, 'images/productos/96d1b5570fcc9a01c824080485a05e6c.jpg', '1', '2020-07-25 12:08:18', 'activo', 'admin'),
(6, 1, 'F-00004', 'OSMOSIS INVERSA 6 ETAPAS 75 GPD', 'OSMOSIS INVERSA 6 ETAPAS 75 GPD', 999.00, 0.00, 'images/productos/5522dea1440a54b40f8bed8a3a3adc8d.jpg', '1', '2020-07-25 12:11:01', 'activo', 'admin'),
(7, 1, 'F-00005', 'OSMOSIS INVERSA 3000 GPD', 'Incluye:\r\nLlave dispensadora.\r\nAccesorios de instalación.\r\nBomba 3 hp vertical\r\nControlador con medidor TDS\r\nMontaje: sobre pared, bajo mesón de cocina o piso.\r\nForro para proteger el equipo.\r\n', 7500.00, 0.00, 'images/productos/d4c1a43b867cdf0ba49b4dc959a96163.jpg', '1', '2020-07-25 12:14:14', 'activo', 'admin'),
(8, 1, 'F-00007', 'ÓSMOSIS INVERSA CL300', 'ÓSMOSIS INVERSA CL300', 1750.00, NULL, 'images/productos/9fb8492b08efe57e5e8dbe5891baa1a9.jpg', '', '2020-07-27 22:34:45', 'inactivo', 'admin'),
(9, 1, 'F-00008', 'ÓSMOSIS INVERSA CL300', 'ÓSMOSIS INVERSA CL300fdghdfsgdsf descriociomn', 1500.00, 0.00, 'images/productos/8cf8d6ae1c3f62d7f06ec3b21e825f8d.jpg', '', '2020-07-27 22:54:53', 'inactivo', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincia`
--

CREATE TABLE `provincia` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `provincia`
--

INSERT INTO `provincia` (`id`, `nombre`, `estado`) VALUES
(1, 'Azuay', 1),
(2, 'Bolivar', 1),
(3, 'Cañar', 1),
(4, 'Carchi', 1),
(5, 'Cotopaxi', 1),
(6, 'Chimborazo', 1),
(7, 'El Oro', 1),
(8, 'Esmeraldas', 1),
(9, 'Guayas', 1),
(10, 'Imbabura', 1),
(11, 'Loja', 1),
(12, 'Los Rios', 1),
(13, 'Manabí', 1),
(14, 'Morona Santiago', 1),
(15, 'Napo', 1),
(16, 'Pastaza', 1),
(17, 'Pichincha', 1),
(18, 'Tungurahua', 1),
(19, 'Zamora Chinchipe', 1),
(20, 'Orellana', 1),
(21, 'Sucumbios', 1),
(22, 'Santo Domingo de los Tsachilas', 1),
(23, 'Santa Elena', 1),
(24, 'Galápagos', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `username`, `password`, `created_at`) VALUES
(1, 'admin', 'admin', 'admin', '$2y$10$ZlMS6VkxY.tcmkkLU4vaf.GLDuGJqiCx9bBa/csAeOjQjXg5lDAtS', '2020-07-20 12:46:16');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `accesorios`
--
ALTER TABLE `accesorios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ciudad_provincia` (`provincia_id`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `envio`
--
ALTER TABLE `envio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ciudad` (`ciudad_id`),
  ADD KEY `FK_envio_orden` (`orden_id`);

--
-- Indices de la tabla `ficha_tecnica`
--
ALTER TABLE `ficha_tecnica`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ficha_tecnica_detalle`
--
ALTER TABLE `ficha_tecnica_detalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ficha_tecnica_detalle_fk_ficha_tecnica` (`fk_ficha_tecnica`);

--
-- Indices de la tabla `ficha_tecnica_detalle_accesorio`
--
ALTER TABLE `ficha_tecnica_detalle_accesorio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ficha_tecnica_detalle_accesorio_fk_accesorio` (`fk_accesorio`),
  ADD KEY `FK_ficha_tecnica_detalle_accesorio_fk_ficha_tecnica_detalle` (`fk_ficha_tecnica_detalle`);

--
-- Indices de la tabla `ficha_tecnica_detalle_filtracion`
--
ALTER TABLE `ficha_tecnica_detalle_filtracion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_ficha_tecnica_detalle_filtracion_fk_ficha_tecnica_detalle` (`fk_ficha_tecnica_detalle`),
  ADD KEY `FK_ficha_tecnica_detalle_filtracion_fk_filtracion` (`fk_filtracion`);

--
-- Indices de la tabla `filtracion`
--
ALTER TABLE `filtracion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `orden`
--
ALTER TABLE `orden`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_orden_cliente` (`cliente_id`);

--
-- Indices de la tabla `orden_detalle`
--
ALTER TABLE `orden_detalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK__producto` (`producto_id`),
  ADD KEY `FK__orden` (`orden_id`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_producto_categoria` (`categoria_id`);

--
-- Indices de la tabla `provincia`
--
ALTER TABLE `provincia`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `accesorios`
--
ALTER TABLE `accesorios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `envio`
--
ALTER TABLE `envio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `ficha_tecnica`
--
ALTER TABLE `ficha_tecnica`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ficha_tecnica_detalle`
--
ALTER TABLE `ficha_tecnica_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ficha_tecnica_detalle_accesorio`
--
ALTER TABLE `ficha_tecnica_detalle_accesorio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ficha_tecnica_detalle_filtracion`
--
ALTER TABLE `ficha_tecnica_detalle_filtracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `filtracion`
--
ALTER TABLE `filtracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `orden`
--
ALTER TABLE `orden`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `orden_detalle`
--
ALTER TABLE `orden_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `provincia`
--
ALTER TABLE `provincia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ficha_tecnica_detalle`
--
ALTER TABLE `ficha_tecnica_detalle`
  ADD CONSTRAINT `FK_ficha_tecnica_detalle_fk_ficha_tecnica` FOREIGN KEY (`fk_ficha_tecnica`) REFERENCES `ficha_tecnica` (`id`) ON DELETE NO ACTION;

--
-- Filtros para la tabla `ficha_tecnica_detalle_accesorio`
--
ALTER TABLE `ficha_tecnica_detalle_accesorio`
  ADD CONSTRAINT `FK_ficha_tecnica_detalle_accesorio_fk_accesorio` FOREIGN KEY (`fk_accesorio`) REFERENCES `accesorios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_ficha_tecnica_detalle_accesorio_fk_ficha_tecnica_detalle` FOREIGN KEY (`fk_ficha_tecnica_detalle`) REFERENCES `ficha_tecnica_detalle` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `ficha_tecnica_detalle_filtracion`
--
ALTER TABLE `ficha_tecnica_detalle_filtracion`
  ADD CONSTRAINT `FK_ficha_tecnica_detalle_filtracion_fk_ficha_tecnica_detalle` FOREIGN KEY (`fk_ficha_tecnica_detalle`) REFERENCES `ficha_tecnica_detalle` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_ficha_tecnica_detalle_filtracion_fk_filtracion` FOREIGN KEY (`fk_filtracion`) REFERENCES `filtracion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
