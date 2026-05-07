/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: 
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0+deb12u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dbbd`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dbbd` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `dbbd`;

--
-- Table structure for table `alert_history`
--

DROP TABLE IF EXISTS `alert_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL,
  `recipient_addr` varchar(50) NOT NULL,
  `delivery_status` enum('sent','failed') DEFAULT 'sent',
  PRIMARY KEY (`id`),
  KEY `token_id` (`token`),
  CONSTRAINT `token_id` FOREIGN KEY (`token`) REFERENCES `triggers` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert_history`
--

LOCK TABLES `alert_history` WRITE;
/*!40000 ALTER TABLE `alert_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `alert_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL,
  `source_ip` varchar(50) NOT NULL,
  `user_agent` varchar(255) NOT NULL,
  `event_time` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `generated_token_id` (`token`),
  CONSTRAINT `generated_token_id` FOREIGN KEY (`token`) REFERENCES `triggers` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts`
--

LOCK TABLES `alerts` WRITE;
/*!40000 ALTER TABLE `alerts` DISABLE KEYS */;
INSERT INTO `alerts` VALUES
(3,'e35a4d0f-aa98-46a1-a8ac-e6ab5095932f','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:43:07'),
(4,'e35a4d0f-aa98-46a1-a8ac-e6ab5095932f','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:46:32'),
(5,'e35a4d0f-aa98-46a1-a8ac-e6ab5095932f','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:47:40'),
(6,'9d51ecde-17aa-4bfc-8f0a-672271e3b226','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:48:15'),
(7,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:54:09'),
(8,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 08:54:15'),
(9,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','PostmanRuntime/7.51.1','2026-04-03 09:14:47'),
(10,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 08:56:26'),
(11,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 08:57:45'),
(12,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 08:58:28'),
(13,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 08:59:25'),
(14,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 09:05:56'),
(15,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 09:12:21'),
(16,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 12:01:42'),
(17,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','127.0.0.1','curl/7.88.1','2026-05-06 13:03:39'),
(18,'b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596','192.168.100.10','Mozilla/5.0','2026-05-06 13:24:28'),
(19,'b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596','192.168.100.10','Mozilla/5.0','2026-05-06 13:25:37'),
(20,'b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596','192.168.100.10','Mozilla/5.0','2026-05-06 19:41:23'),
(21,'b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596','192.168.100.10','Mozilla/5.0','2026-05-06 19:41:27');
/*!40000 ALTER TABLE `alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `baits`
--

DROP TABLE IF EXISTS `baits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `baits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `abbrev` varchar(10) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `bait_path` varchar(255) NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `baits`
--

LOCK TABLES `baits` WRITE;
/*!40000 ALTER TABLE `baits` DISABLE KEYS */;
INSERT INTO `baits` VALUES
(1,'Word Document','DOCX','file','Decoy DOCX file with a token to detect unauthorised access and opening','static/baits/docx/','static/baits/images/docx.png'),
(2,'Excel Spreadsheet Bait','XLSX','file','Decoy XLSX file with a bait to detect unauthorised access','static/baits/xlsx/','static/baits/images/xlsx.png'),
(3,'PowerPoint Presentation Bait','PPTX','file','Decoy PPTX file with a canary token to detect unauthorised access','static/baits/pptx/','static/baits/images/pptx.png'),
(4,'PDF Document Bait','PDF','file','Decoy PDF file embedded with a token to detect unauthorised access','static/baits/pdf/','static/baits/images/pdf.png'),
(5,'QR Code Bait','QR','qrcode','Decoy QR code token that triggers an alert when scanned by an unauthorised user','static/baits/qr/','static/baits/images/qr.png'),
(6,'Folder Integrity Monitor','FIM','folder','Monitors a decoy folder for unauthorised access or modification using Windows Event ID 4663','static/baits/fim/','static/baits/images/fim.png'),
(7,'Domain Token Bait','DOMAIN','domain','Decoy domain token that triggers a DNS/HTTP callback when accessed by an unauthorised user','static/baits/domain/','static/baits/images/domain.png'),
(8,'My SQL Dump','MYSQL_DUMP','Database','A SQL Database Dump that when loaded. It triggers an alert to the specified email','static/baits/mysql','static/baits/images/mysql.png');
/*!40000 ALTER TABLE `baits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mysql_events`
--

DROP TABLE IF EXISTS `mysql_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mysql_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL,
  `user` varchar(50) NOT NULL,
  `hostname` varchar(50) NOT NULL,
  `db_name` varchar(50) NOT NULL,
  `source_ip` varchar(50) NOT NULL,
  `event_time` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `db_token_id` (`token`),
  CONSTRAINT `db_token_id` FOREIGN KEY (`token`) REFERENCES `triggers` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mysql_events`
--

LOCK TABLES `mysql_events` WRITE;
/*!40000 ALTER TABLE `mysql_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `mysql_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `triggers`
--

DROP TABLE IF EXISTS `triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `triggers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL,
  `reminder` varchar(255) NOT NULL,
  `callback_email` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `bait_id` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `trigger_token_unique` (`token`),
  KEY `users_id` (`user_id`),
  KEY `baitz_id` (`bait_id`),
  CONSTRAINT `baitz_id` FOREIGN KEY (`bait_id`) REFERENCES `baits` (`id`),
  CONSTRAINT `users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `triggers`
--

LOCK TABLES `triggers` WRITE;
/*!40000 ALTER TABLE `triggers` DISABLE KEYS */;
INSERT INTO `triggers` VALUES
(3,'aea32a82-80b6-4b47-831d-e008f0299522','Bait To trigger Alert When The Powerpoint is Opened','adverse@test.com',6,3,'2026-03-30 22:06:35'),
(4,'da00bab5-e440-462e-a21d-ead819278f3f','Bait To trigger Alert When The Powerpoint is Opened','adverse@test.com',6,3,'2026-03-30 22:07:25'),
(7,'cc28c04a-92e4-4cb6-aeb5-a759c5ebaefa','Bait To trigger Alert When The Powerpoint is Opened','attackers@attackers.com',6,3,'2026-03-30 22:54:12'),
(9,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MS Office Document Bait','anonymouse@gmail.com',6,2,'2026-03-30 22:57:44'),
(10,'e35a4d0f-aa98-46a1-a8ac-e6ab5095932f','File Intergity Monitoring on the Domain Controller','adverse@test.com',6,7,'2026-03-30 23:53:29'),
(15,'9d51ecde-17aa-4bfc-8f0a-672271e3b226','Catching Insiders that Open it','administrator@test.com',8,4,'2026-04-03 06:16:57'),
(19,'357f6dcf-7d07-473c-8026-634a94271b99','This is added for test purposes.','administrator@test.com',8,4,'2026-05-05 19:16:03'),
(20,'57bd1d4c-46d3-449c-9e76-9c9e0f7cdb49','This is added for test purposes.','administrator@test.com',8,4,'2026-05-05 19:16:06'),
(22,'72fb85d0-1525-44cf-8974-45d291b11933','This is added for test purposes.','administrator@test.com',8,4,'2026-05-05 19:16:11'),
(23,'dff00d04-818d-48d3-8923-0729be39ec04','This is added for test purposes.','adverse@test.com',6,4,'2026-05-05 19:17:14'),
(24,'336ec056-6f8b-40f1-8193-d078570bfbe1','This is added for test purposes.','adverse@test.com',6,4,'2026-05-05 19:17:17'),
(26,'00633498-f57f-4269-88c6-2d85fe990b81','This is added for test purposes.','adverse@test.com',6,4,'2026-05-05 19:17:25'),
(27,'51f3a4a5-1f77-4876-aada-6f2d1c069307','Placed in Data center','administrator@test.com',8,2,'2026-05-06 06:56:43'),
(28,'c4aa4ecc-1273-4f0f-9889-f04c72063027','Word Document Bait By For boardroom','anzo@gmail.com',15,1,'2026-05-06 07:01:35'),
(29,'0797fda0-ef24-4ba1-b7be-f8921f9cdf84','Monitor changes to a bait directory likely to be accessed by an incider','anzo@gmail.com',15,6,'2026-05-06 07:02:13'),
(31,'b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596','Word Document Deployed on the Linux Server Patiently waiting for for anyone to open.','benardtera2@gmail.com',6,1,'2026-05-06 13:10:05');
/*!40000 ALTER TABLE `triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin','012230053@isbatuniversity.com','admin@1234'),
(2,'admin','admin@dbbd.com','admin@1234'),
(3,'Java','Java@java.com','pbkdf2:sha256:260000$QQRIKgPurR18z4ni$03d72e464905631aedb36c0d0b3d52032e185a3d6d19c2a684ce52b32f7608de'),
(4,'python','python@java.com','pbkdf2:sha256:260000$1hwWgM7PTaZdC6cE$65183762411ccb5dd72806f77eaefb3feadc50c5a1b8c28c10719ea0af072367'),
(5,'cpp','cpp@java.com','pbkdf2:sha256:260000$qFK7f3GqEWMWJIO3$b0b709414e41addac8722ad404e42ac26c116f7fc57766f1d6aded62cf26544a'),
(6,'adverse','adverse@test.com','pbkdf2:sha256:260000$z5yoIbfTtFE34HQI$474fd02678747cb94441e91dbc3dc273c6f078205d70f3f45b914ff4528bd0b2'),
(7,'snowden','snowden@test.com','pbkdf2:sha256:260000$52Ec5QzkDjwtXqF2$b0c4238a715368f6616d461ff921abee8515b448b0aab8663e3336817fa76b73'),
(8,'administrator','administrator@test.com','pbkdf2:sha256:260000$2PpdQ41cTLoocyoN$079610a395cbed23101e3a00f61748b5af3c000ecae4439a446c082f59986fad'),
(9,'analyst','analyst@analyst.com','pbkdf2:sha256:260000$Oc8RVTnH7bBpYsw3$c7a58197b948da540499d57bc5b9d89e56b79a2214a96bae754c59a963a3e960'),
(10,'anzo','benardtera2@gmail.com','pbkdf2:sha256:260000$D7FahpsJevJIID6A$dfc6f7dc94a286546dd1f4f2e73d03980411b43b521c2bd4f5e2d193b2a3e254'),
(11,'adversary','adversary@admin.com','pbkdf2:sha256:260000$g0dnWMDOMtwIPBcC$ecd8831a74feea4771385be0c9ca6dc6b619a825b55ec3d0d24ec075ae9f3707'),
(12,'attacker','attacker@attacker.com','pbkdf2:sha256:260000$vSFYbR3E520tz63s$a2f66185fcbb6530c729894df748cc9d550f86696b16415d95c5efa9a144ecf5'),
(13,'creaper','creaper@creaper.com','pbkdf2:sha256:260000$YLYFMkznUnSnMVPQ$5bd4097676bd1aad98e7d7e192d96201587b0e889b117892b77e8df55169bd38'),
(14,'abdul','abdul@gmailc.om','pbkdf2:sha256:260000$E5dOze8rQsDZ60gm$63401e1e1f9be4ea49352ce048c65e864f4e8dfbb66474049bf07a45320bd1f7'),
(15,'benard','anzo@gmail.com','pbkdf2:sha256:260000$mbQjkjlN2Ea8l3kt$c2fef4fbf245df06b70e1ac328c03f0e4c7f4e3f3f9598e46cbb59e35c2be843');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watcher_events`
--

DROP TABLE IF EXISTS `watcher_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `watcher_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(50) NOT NULL,
  `user` varchar(50) NOT NULL,
  `path` varchar(255) NOT NULL,
  `access` varchar(50) NOT NULL,
  `process` varchar(255) NOT NULL,
  `source_ip` varchar(50) NOT NULL,
  `event_time` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `matching_token_id` (`token`),
  CONSTRAINT `matching_token_id` FOREIGN KEY (`token`) REFERENCES `triggers` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watcher_events`
--

LOCK TABLES `watcher_events` WRITE;
/*!40000 ALTER TABLE `watcher_events` DISABLE KEYS */;
INSERT INTO `watcher_events` VALUES
(1,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','0x400','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-03-04 22:33:12'),
(2,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','Execute / Traverse','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-03-04 22:33:01'),
(3,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:07:15'),
(4,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\dir','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:07:15'),
(5,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\test','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:07:15'),
(6,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:07:16'),
(7,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\System32\\cmd.exe','192.168.20.3','2026-04-13 14:09:41'),
(8,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB.jpg','WriteData / AddFile','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:20:44'),
(9,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB.jpg','AppendData / AddSubdir','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:20:44'),
(10,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:02'),
(11,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\dir','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:02'),
(12,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\test','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:02'),
(13,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB.jpg','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:06'),
(14,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:06'),
(15,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB - Copy.jpg','WriteData / AddFile','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:24:08'),
(16,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB - Copy.jpg','AppendData / AddSubdir','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:24:08'),
(17,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:09'),
(18,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\dir','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:09'),
(19,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\test','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:24:09'),
(20,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:25:37'),
(21,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\NEXUS HUB - Copy.jpg','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:25:37'),
(22,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','WriteData / AddFile','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:34:02'),
(23,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\System32\\dllhost.exe','192.168.20.3','2026-04-13 14:34:02'),
(24,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:18'),
(25,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:21'),
(26,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\dir','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:21'),
(27,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential\\test','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:21'),
(28,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:26'),
(29,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','MTC 1','C:\\Program Files (x86)\\confidential','ListDirectory / ReadData','C:\\Windows\\explorer.exe','192.168.20.3','2026-04-13 14:35:35'),
(30,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','Execute / Traverse','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-05-05 22:33:01'),
(31,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','Execute / Traverse','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-05-05 22:32:01'),
(32,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','Execute / Traverse','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-05-06 22:32:01'),
(33,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','Execute / Traverse','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-05-06 22:32:21'),
(34,'2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a','Administrator','C:\\Program Files (x86)\\confidential','0x500','C:\\Program Files (x86)\\powershell\\powershell.exe','127.0.0.1','2026-05-06 22:32:21');
/*!40000 ALTER TABLE `watcher_events` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-07 10:23:54
