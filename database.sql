-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: test_db_7
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `analisis`
--

DROP TABLE IF EXISTS `analisis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analisis` (
  `id_analisis` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `id_escuela` int DEFAULT NULL,
  `id_ciclo` int DEFAULT NULL,
  `id_grado` int DEFAULT NULL,
  `id_grupo` int DEFAULT NULL,
  `num_total_actores` int DEFAULT NULL,
  `actores_mapeados` int DEFAULT NULL,
  `num_relaciones` int DEFAULT NULL,
  `densidad` decimal(5,3) DEFAULT NULL,
  `diametro` int DEFAULT NULL,
  `cercania` decimal(5,3) DEFAULT NULL,
  `promedio_grado` decimal(5,3) DEFAULT NULL,
  PRIMARY KEY (`id_analisis`),
  KEY `id_escuela` (`id_escuela`),
  KEY `id_ciclo` (`id_ciclo`),
  KEY `id_grado` (`id_grado`),
  KEY `id_grupo` (`id_grupo`),
  CONSTRAINT `analisis_ibfk_1` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`),
  CONSTRAINT `analisis_ibfk_2` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos` (`id_ciclo`),
  CONSTRAINT `analisis_ibfk_3` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`),
  CONSTRAINT `analisis_ibfk_4` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `autonomia`
--

DROP TABLE IF EXISTS `autonomia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autonomia` (
  `id_autonomia` int NOT NULL AUTO_INCREMENT,
  `autonomia_inicial` decimal(5,2) DEFAULT NULL,
  `autonomia_final` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_autonomia`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ayudapercibidaaux`
--

DROP TABLE IF EXISTS `ayudapercibidaaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ayudapercibidaaux` (
  `id_ayuda` int NOT NULL AUTO_INCREMENT,
  `id_analisis` int DEFAULT NULL,
  `valor` int DEFAULT NULL,
  `porcentaje` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_ayuda`),
  KEY `id_analisis` (`id_analisis`),
  CONSTRAINT `ayudapercibidaaux_ibfk_1` FOREIGN KEY (`id_analisis`) REFERENCES `analisis` (`id_analisis`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ciclos`
--

DROP TABLE IF EXISTS `ciclos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciclos` (
  `id_ciclo` int NOT NULL AUTO_INCREMENT,
  `rango_anual` varchar(255) NOT NULL,
  PRIMARY KEY (`id_ciclo`),
  UNIQUE KEY `rango_anual` (`rango_anual`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `confianzapercibidaaux`
--

DROP TABLE IF EXISTS `confianzapercibidaaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `confianzapercibidaaux` (
  `id_confianza` int NOT NULL AUTO_INCREMENT,
  `id_analisis` int DEFAULT NULL,
  `valor` int DEFAULT NULL,
  `porcentaje` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_confianza`),
  KEY `id_analisis` (`id_analisis`),
  CONSTRAINT `confianzapercibidaaux_ibfk_1` FOREIGN KEY (`id_analisis`) REFERENCES `analisis` (`id_analisis`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `escuelas`
--

DROP TABLE IF EXISTS `escuelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escuelas` (
  `id_escuela` int NOT NULL AUTO_INCREMENT,
  `nombre_escuela` varchar(255) NOT NULL,
  PRIMARY KEY (`id_escuela`),
  UNIQUE KEY `nombre_escuela` (`nombre_escuela`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes` (
  `id_estudiante` int NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(255) NOT NULL,
  `nombre_canonico` varchar(255) NOT NULL,
  `id_escuela` int DEFAULT NULL,
  `id_ciclo` int DEFAULT NULL,
  `id_grado` int DEFAULT NULL,
  `id_grupo` int DEFAULT NULL,
  PRIMARY KEY (`id_estudiante`),
  KEY `id_escuela` (`id_escuela`),
  KEY `id_ciclo` (`id_ciclo`),
  KEY `id_grado` (`id_grado`),
  KEY `id_grupo` (`id_grupo`),
  CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`),
  CONSTRAINT `estudiantes_ibfk_2` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos` (`id_ciclo`),
  CONSTRAINT `estudiantes_ibfk_3` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`),
  CONSTRAINT `estudiantes_ibfk_4` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estudiantesmapeo`
--

DROP TABLE IF EXISTS `estudiantesmapeo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantesmapeo` (
  `id_mapeo` int NOT NULL AUTO_INCREMENT,
  `extra_id` int DEFAULT NULL,
  `id_estudiante` int DEFAULT NULL,
  `id_escuela` int DEFAULT NULL,
  `id_ciclo` int DEFAULT NULL,
  `id_grado` int DEFAULT NULL,
  `id_grupo` int DEFAULT NULL,
  `grado_entrada` int DEFAULT NULL,
  `grado_salida` int DEFAULT NULL,
  `centralidad` decimal(5,3) DEFAULT NULL,
  `percepcion_relacional` varchar(255) DEFAULT NULL,
  `percepcion_conductual` varchar(255) DEFAULT NULL,
  `percepcion_academica` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_mapeo`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_escuela` (`id_escuela`),
  KEY `id_ciclo` (`id_ciclo`),
  KEY `id_grado` (`id_grado`),
  KEY `id_grupo` (`id_grupo`),
  CONSTRAINT `estudiantesmapeo_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  CONSTRAINT `estudiantesmapeo_ibfk_2` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`),
  CONSTRAINT `estudiantesmapeo_ibfk_3` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos` (`id_ciclo`),
  CONSTRAINT `estudiantesmapeo_ibfk_4` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`),
  CONSTRAINT `estudiantesmapeo_ibfk_5` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gradoaux`
--

DROP TABLE IF EXISTS `gradoaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gradoaux` (
  `id_grado_aux` int NOT NULL AUTO_INCREMENT,
  `id_analisis` int DEFAULT NULL,
  `nombre_entrada` varchar(255) DEFAULT NULL,
  `grado_entrada` int DEFAULT NULL,
  `nombre_salida` varchar(255) DEFAULT NULL,
  `grado_salida` int DEFAULT NULL,
  PRIMARY KEY (`id_grado_aux`),
  KEY `id_analisis` (`id_analisis`),
  CONSTRAINT `gradoaux_ibfk_1` FOREIGN KEY (`id_analisis`) REFERENCES `analisis` (`id_analisis`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grados`
--

DROP TABLE IF EXISTS `grados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grados` (
  `id_grado` int NOT NULL AUTO_INCREMENT,
  `nivel_grado` varchar(10) NOT NULL,
  `id_escuela` int DEFAULT NULL,
  PRIMARY KEY (`id_grado`),
  UNIQUE KEY `nivel_grado` (`nivel_grado`),
  KEY `id_escuela` (`id_escuela`),
  CONSTRAINT `grados_ibfk_1` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grupos`
--

DROP TABLE IF EXISTS `grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos` (
  `id_grupo` int NOT NULL AUTO_INCREMENT,
  `nombre_grupo` varchar(10) NOT NULL,
  `id_grado` int DEFAULT NULL,
  PRIMARY KEY (`id_grupo`),
  KEY `id_grado` (`id_grado`),
  CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `modularidadaux`
--

DROP TABLE IF EXISTS `modularidadaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modularidadaux` (
  `id_modularidad` int NOT NULL AUTO_INCREMENT,
  `id_analisis` int DEFAULT NULL,
  `total_comunidades` int DEFAULT NULL,
  `comunidad_cuenta` int DEFAULT NULL,
  `comunidad_tam` int DEFAULT NULL,
  PRIMARY KEY (`id_modularidad`),
  KEY `id_analisis` (`id_analisis`),
  CONSTRAINT `modularidadaux_ibfk_1` FOREIGN KEY (`id_analisis`) REFERENCES `analisis` (`id_analisis`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `perfilesescolares`
--

DROP TABLE IF EXISTS `perfilesescolares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfilesescolares` (
  `id_perfil_esc` int NOT NULL AUTO_INCREMENT,
  `id_escuela` int DEFAULT NULL,
  `id_ciclo` int DEFAULT NULL,
  `id_grado` int DEFAULT NULL,
  `id_grupo` int DEFAULT NULL,
  `autodominio_inicial` decimal(5,2) DEFAULT NULL,
  `automotivacion_inicial` decimal(5,2) DEFAULT NULL,
  `autoconocimiento_inicial` decimal(5,2) DEFAULT NULL,
  `autoestima_inicial` decimal(5,2) DEFAULT NULL,
  `relaciones_interpersonales_inicial` decimal(5,2) DEFAULT NULL,
  `autodominio_final` decimal(5,2) DEFAULT NULL,
  `automotivacion_final` decimal(5,2) DEFAULT NULL,
  `autoconocimiento_final` decimal(5,2) DEFAULT NULL,
  `autoestima_final` decimal(5,2) DEFAULT NULL,
  `relaciones_interpersonales_final` decimal(5,2) DEFAULT NULL,
  `id_promedio` int DEFAULT NULL,
  `id_autonomia` int DEFAULT NULL,
  PRIMARY KEY (`id_perfil_esc`),
  KEY `id_escuela` (`id_escuela`),
  KEY `id_ciclo` (`id_ciclo`),
  KEY `id_grado` (`id_grado`),
  KEY `id_grupo` (`id_grupo`),
  KEY `id_promedio` (`id_promedio`),
  KEY `id_autonomia` (`id_autonomia`),
  CONSTRAINT `perfilesescolares_ibfk_1` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`),
  CONSTRAINT `perfilesescolares_ibfk_2` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos` (`id_ciclo`),
  CONSTRAINT `perfilesescolares_ibfk_3` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`),
  CONSTRAINT `perfilesescolares_ibfk_4` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`),
  CONSTRAINT `perfilesescolares_ibfk_5` FOREIGN KEY (`id_promedio`) REFERENCES `promediototal` (`id_promedio`),
  CONSTRAINT `perfilesescolares_ibfk_6` FOREIGN KEY (`id_autonomia`) REFERENCES `autonomia` (`id_autonomia`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `perfilesestudiantiles`
--

DROP TABLE IF EXISTS `perfilesestudiantiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfilesestudiantiles` (
  `id_perfil_est` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int DEFAULT NULL,
  `autodominio` decimal(5,2) DEFAULT NULL,
  `automotivacion` decimal(5,2) DEFAULT NULL,
  `autoconocimiento` decimal(5,2) DEFAULT NULL,
  `autoestima` decimal(5,2) DEFAULT NULL,
  `relaciones_interpersonales_sanas` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_perfil_est`),
  KEY `id_estudiante` (`id_estudiante`),
  CONSTRAINT `perfilesestudiantiles_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`)
) ENGINE=InnoDB AUTO_INCREMENT=465 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `promediototal`
--

DROP TABLE IF EXISTS `promediototal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promediototal` (
  `id_promedio` int NOT NULL AUTO_INCREMENT,
  `autodominio_inicial` decimal(5,2) DEFAULT NULL,
  `automotivacion_inicial` decimal(5,2) DEFAULT NULL,
  `autoconocimiento_inicial` decimal(5,2) DEFAULT NULL,
  `autoestima_inicial` decimal(5,2) DEFAULT NULL,
  `relaciones_interpersonales_inicial` decimal(5,2) DEFAULT NULL,
  `autodominio_final` decimal(5,2) DEFAULT NULL,
  `automotivacion_final` decimal(5,2) DEFAULT NULL,
  `autoconocimiento_final` decimal(5,2) DEFAULT NULL,
  `autoestima_final` decimal(5,2) DEFAULT NULL,
  `relaciones_interpersonales_final` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_promedio`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `servicioestudiantes`
--

DROP TABLE IF EXISTS `servicioestudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicioestudiantes` (
  `id_servicio_estudiante` int NOT NULL AUTO_INCREMENT,
  `id_servicio` int DEFAULT NULL,
  `id_estudiante` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio_estudiante`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_estudiante` (`id_estudiante`),
  CONSTRAINT `servicioestudiantes_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`),
  CONSTRAINT `servicioestudiantes_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(255) NOT NULL,
  `modalidad` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `id_escuela` int DEFAULT NULL,
  `id_ciclo` int DEFAULT NULL,
  `id_grado` int DEFAULT NULL,
  `id_grupo` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio`),
  KEY `id_escuela` (`id_escuela`),
  KEY `id_ciclo` (`id_ciclo`),
  KEY `id_grado` (`id_grado`),
  KEY `id_grupo` (`id_grupo`),
  CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`id_escuela`) REFERENCES `escuelas` (`id_escuela`),
  CONSTRAINT `servicios_ibfk_2` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos` (`id_ciclo`),
  CONSTRAINT `servicios_ibfk_3` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id_grado`),
  CONSTRAINT `servicios_ibfk_4` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'test_db_7'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-14 19:16:40
