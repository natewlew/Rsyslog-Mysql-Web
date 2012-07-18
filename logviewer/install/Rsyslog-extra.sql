/*
This file is part of Rsyslog Mysql Web, Copyright 2012 Nathan Lewis <natewlew@gmail.com>

    Rsyslog Mysql Web is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    Rsyslog Mysql Web is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Rsyslog Mysql Web.  If not, see <http://www.gnu.org/licenses/>.
*/

-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 05, 2012 at 04:40 AM
-- Server version: 5.5.24
-- PHP Version: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Rsyslog`
--

-- --------------------------------------------------------

--
-- Table structure for table `facilities`
--

CREATE TABLE IF NOT EXISTS `facilities` (
  `id` tinyint(4) NOT NULL,
  `facility` varchar(28) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `facilities`
--

INSERT INTO `facilities` (`id`, `facility`) VALUES
(0, 'kernel'),
(1, 'user-level'),
(2, 'mail'),
(3, 'system daemons'),
(4, 'security/authorization'),
(5, 'messages generated'),
(6, 'line printer subsystem'),
(7, 'network news subsystem'),
(8, 'UUCP subsystem'),
(9, 'clock daemon'),
(10, 'security/authorization'),
(11, 'FTP daemon'),
(12, 'NTP subsystem'),
(13, 'log audit'),
(14, 'log alert'),
(15, 'clock daemon'),
(16, 'local0'),
(17, 'local1'),
(18, 'Local2'),
(19, 'local3'),
(20, 'local4'),
(21, 'local5'),
(22, 'local6'),
(23, 'local7');

-- --------------------------------------------------------

--
-- Table structure for table `priorites`
--

CREATE TABLE IF NOT EXISTS `priorites` (
  `num` tinyint(4) NOT NULL,
  `severity` varchar(18) NOT NULL,
  PRIMARY KEY (`num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `priorites`
--

INSERT INTO `priorites` (`num`, `severity`) VALUES
(0, 'Emergency'),
(1, 'Alert'),
(4, 'Warning'),
(2, 'Critical'),
(3, 'Error'),
(5, 'Notice'),
(6, 'Informational'),
(7, 'Debug');

--
-- Create Indexes on System Events
--
CREATE INDEX `DeviceReportedTime_Index` ON SystemEvents (`DeviceReportedTime`,`Facility`,`Priority`,`FromHost`,`SysLogTag`);
CREATE FULLTEXT INDEX `Message_Index` ON SystemEvents (`Message`);
  
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
