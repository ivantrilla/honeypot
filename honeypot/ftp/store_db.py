#!/usr/bin/env python3
import mariadb
import datetime
import sys

class Database:
    # data will store only one user, and the amount of times that has been logged within that period of ~5s
    # the action variable can hold 3 different values: user, fail, download
    def __init__(self, data, action):

    
        try: 

            conn = mariadb.connect(
                    user="user1",
                    password="password1",
                    host="127.0.0.1",  
                    port=3306,
                    database="Logs"
                    )
            
            cur = conn.cursor()

            # depending on the action it'll have to save different stuff

            if action == "user":
                for user, amount in data.items():
                    self.user = user
                    self.amount = amount
                self.successful_login(cur)

            elif action == "download":
                self.amount = data["amount"]
                self.download(cur)

            else: # this is for login_error attempts
                for user,_ in data.items():
                    self.user = user
                self.failed_login(cur)

            conn.commit()


        # print and log any kind of error message pops up 

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

            with open("mysql_error.log", "a") as f:
                f.write(f"Error connecting to MariaDB Platform: {e}\n")
            sys.exit(1)

        # Ensure the connection is closed
        finally:
            if conn:
                cur.close()
                conn.close()

    def successful_login(self, cur):

        # just grab a dateframe of last login

        dateframe =  str(datetime.datetime.now())
  
        # I previosuly need to fetch amount of previous logins to add the new ones    
        # admin will have ID 1
        if self.user == "admin":

            cur.execute("SELECT amount FROM FTPSuccess WHERE ID=1")
            for elem in cur:
                amount = elem[0]

            self.amount+=amount
            cur.execute("update FTPSuccess set amount = ?, last_time = ? where Id = 1", (self.amount, dateframe)) 
                    
        #anonymous user will have ID 2
        else:
            cur.execute("SELECT amount FROM FTPSuccess WHERE ID=2")
            for elem in cur:
                amount = elem[0]

            self.amount+=amount
            cur.execute("update FTPSuccess set amount = ?, last_time = ? where Id = 2", (self.amount, dateframe))

    def failed_login(self, cur):

        dateframe = str(datetime.datetime.now())

        cur.execute("insert into FTPError (username, last_time) values (?,?)", (self.user, dateframe))
                    

    def download(self, cur):
  
        dateframe =  str(datetime.datetime.now())

        cur.execute("SELECT amount FROM BaitDownload")
        for elem in cur:
            amount = elem[0]

        self.amount+=amount
        cur.execute("update BaitDownload set last_time = ?, amount = ?", (dateframe, self.amount))



# mariadb Logs dump to undertand how code interacts with existing tables
"""


-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Logs
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

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
-- Table structure for table `BaitDownload`
--

DROP TABLE IF EXISTS `BaitDownload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BaitDownload` (
  `amount` int(11) DEFAULT NULL,
  `last_time` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BaitDownload`
--

LOCK TABLES `BaitDownload` WRITE;
/*!40000 ALTER TABLE `BaitDownload` DISABLE KEYS */;
INSERT INTO `BaitDownload` VALUES
(3,'2024-11-21 12:56:25.228794');
/*!40000 ALTER TABLE `BaitDownload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FTPError`
--

DROP TABLE IF EXISTS `FTPError`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FTPError` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `last_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FTPError`
--

LOCK TABLES `FTPError` WRITE;
/*!40000 ALTER TABLE `FTPError` DISABLE KEYS */;
INSERT INTO `FTPError` VALUES
(1,'random','2024-11-21 15:07:00.422661'),
(2,'administrator','2024-11-21 15:07:20.430120');
/*!40000 ALTER TABLE `FTPError` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FTPSuccess`
--

DROP TABLE IF EXISTS `FTPSuccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FTPSuccess` (
  `ID` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `amount` int(11) DEFAULT NULL,
  `last_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FTPSuccess`
--

LOCK TABLES `FTPSuccess` WRITE;
/*!40000 ALTER TABLE `FTPSuccess` DISABLE KEYS */;
INSERT INTO `FTPSuccess` VALUES
(1,'admin',4,'2024-11-21 12:56:20.221527'),
(2,'anonymous',7,'2024-11-21 15:07:40.437317');
/*!40000 ALTER TABLE `FTPSuccess` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-21 15:08:49

"""