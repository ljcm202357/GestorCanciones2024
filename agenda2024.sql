-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-03-2024 a las 02:55:50
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agenda2024`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `canciones`
--

CREATE TABLE `canciones` (
  `song_id` int(11) NOT NULL,
  `title` varchar(20) NOT NULL,
  `artist` varchar(50) NOT NULL,
  `genre` varchar(20) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `duration` varchar(10) NOT NULL,
  `alanzamiento` varchar(10) NOT NULL,
  `img` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `canciones`
--

INSERT INTO `canciones` (`song_id`, `title`, `artist`, `genre`, `price`, `duration`, `alanzamiento`, `img`) VALUES
(3, 'Mañana sera bonito', 'karol g', 'reggeton', 20000, '3 minutos', '2023-01-02', ''),
(6, 'amor amor amor etern', 'ducal', 'rock', 9000, '3', '1983-03-09', 0x436170747572612064652070616e74616c6c6120323032332d30372d3137203136303732372e706e67),
(7, 'tacones rojos', 'yatra', 'pop', 10000, '4', '1990-02-08', 0x436170747572612064652070616e74616c6c6120323032332d30372d3137203134323130312e706e67);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

CREATE TABLE `personas` (
  `idper` int(11) NOT NULL,
  `nombreper` varchar(60) NOT NULL,
  `apellidoper` varchar(60) NOT NULL,
  `emailper` varchar(60) NOT NULL,
  `dirper` varchar(60) NOT NULL,
  `telper` varchar(20) NOT NULL,
  `usuarioper` varchar(60) NOT NULL,
  `contraper` varchar(255) NOT NULL,
  `roles` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`idper`, `nombreper`, `apellidoper`, `emailper`, `dirper`, `telper`, `usuarioper`, `contraper`, `roles`) VALUES
(30, 'felipe', 'gomez', 'felipe2024@gmail.com', 'altillos de la campiña', '3153693006', 'felipe2024', 'scrypt:32768:8:1$UoRfxkGyH13zTSxV$8f96cf9756d49625677bd3fd3caaf107f27dc1f6eb58d678a0f7f1760872235fd6b4cedc34fbfc62a1b335b3a449b8778f10cfce325ac4813cde6ad273d5dc3e', ''),
(32, 'Lucy', 'Cuervo', 'cuervo@gmail.com', 'altillos de la campiña', '78945821', 'lucy2024', 'scrypt:32768:8:1$JQzjPUjDdsahKvKO$4ac27aead543e32bf65c0d5eac6e2647eec7a4785388412ba0c732c62f08f9cc74be2db628e8bc2f2d63d9dc018309e3a0f182c2ad00d13dbfb7e316823f9423', ''),
(33, 'tata', 'martinez', 'mar@gmail.com', 'versalles', '2669032', 'tata2024', 'scrypt:32768:8:1$igA2qYuLFUQXeEdJ$f1856f7bad64cd33fcd7158b21421a825fb29120667322411d523a097efbc1f98b7b6c072d1c7c81cba90eb9b3f70891671de9a8c53c5a45096f5a7f32918945', ''),
(34, 'Johanna', 'Cifuentes', 'martinez@gmail.com', 'versalles', '7849545', 'martinez2024', 'scrypt:32768:8:1$2JuojnUQfEQPDQGg$f115649933b16af24f7f70ed9aa1e2bc642a24b7ea354f2954b56a67e8920f80733bcc0d2b9fea77fa0c023d734fa1cd6158b782c2fb84c2dd2bd50bc1594792', 'administrador'),
(35, 'leidy', 'cifuentes', 'leidyc17@gmail.com', 'der', '32189894', 'leidyc17', 'scrypt:32768:8:1$22MgKYVo9tGBUaav$3e259d7d580cc80d073401a573db719ebf1a5e11c911d33e9d6e6815535d64fe13420e0c4c336b048e024e5bb31fa0eff17ec61e1901af36f3c1096bd6233dd1', 'comprador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `canciones`
--
ALTER TABLE `canciones`
  ADD PRIMARY KEY (`song_id`);

--
-- Indices de la tabla `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`idper`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `canciones`
--
ALTER TABLE `canciones`
  MODIFY `song_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `personas`
--
ALTER TABLE `personas`
  MODIFY `idper` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
