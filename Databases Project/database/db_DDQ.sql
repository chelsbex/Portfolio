-- phpMyAdmin SQL Dump
-- version 5.1.1-1.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 22, 2021 at 05:38 PM
-- Server version: 10.4.20-MariaDB-log
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_beckche`
--

-- --------------------------------------------------------

--
-- Table structure for table `Categories`
--

CREATE TABLE `Categories` (
  `categoryID` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`categoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Categories`
--

INSERT INTO `Categories` (`categoryID`, `name`) VALUES
(0, 'Savory Food'),
(1, 'Sweet Food'),
(2, 'Wine'),
(3, 'Non-Alcoholic Beverage'),
(4, 'Soap'),
(5, 'Candle'),
(6, 'Lotion'),
(7, 'Misc Bath'),
(8, 'Accessories'),
(9, 'Decor');

-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--

CREATE TABLE `Customers` (
  `customerID` int(5) NOT NULL AUTO_INCREMENT,
  `fname` varchar(255) NOT NULL,
  `lname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phoneNumber` varchar(15) DEFAULT NULL,
  `streetAddress` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(2) NOT NULL,
  `countryCode` int(3) NOT NULL,
  `acceptingEmails` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`customerID`, `fname`, `lname`, `email`, `phoneNumber`, `streetAddress`, `city`, `state`, `countryCode`, `acceptingEmails`) VALUES
(0, 'Kim', 'Walton', 'kwal_44@gmail.com', '(469)421-3234', '1467 Meadowlark Dr. \r\n', 'Dallas', 'TX', 840, 0),
(1, 'Curtis', 'Partridge', 'curtisss@hotmail.com', '(310)445-8966', '680 Centennial Ln. ', 'Los Angeles', 'CA', 840, 1),
(2, 'Jeremiah', 'Ortiz', 'jereortiz@yahoo.com', '(312)566-3218', '4315 Grassy Knoll Dr. ', 'Chicago', 'IL', 840, 0),
(3, 'Andrea', 'Lemieux', 'mslemieux@gmail.com', '(206)421-5578', '78005 Acorn Park Dr.', 'Seattle', 'WA', 840, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--

CREATE TABLE `Products` (
  `productID` int(5) NOT NULL AUTO_INCREMENT,
  `vid` int(5) NOT NULL,
  `catid` int(5) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `companyCost` decimal(10,2) NOT NULL,
  `salePrice` decimal(10,2) NOT NULL,
  `expirationDate` date DEFAULT NULL,
  `stockQuant` int(10) NOT NULL DEFAULT 0,
  PRIMARY KEY (`productID`),
  KEY `pvid` (`vid`),
  KEY `pcatid` (`catid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`productID`, `vid`, `catid`, `name`, `companyCost`, `salePrice`, `expirationDate`, `stockQuant`) VALUES
(0, 0, 9, 'Lone Daisy - Window Ornament', '10.49', '17.99', NULL, 6),
(1, 0, 9, 'Orange Pumpkin Figurine', '8.99', '14.99', NULL, 10),
(2, 1, 7, 'Purple Lavender Glitter Bomb', '1.39', '4.99', NULL, 8),
(3, 1, 7, 'Fizzy Lemon Lime Bomb', '1.39', '4.99', NULL, 8),
(4, 2, 0, '200 Day Goat Gouda', '3.29', '8.99', '2021-10-12', 12),
(5, 2, 0, 'Fog\'s Bluff Cow Fontina', '4.16', '8.49', '2021-12-15', 12),
(6, 3, 9, 'Spaghetti and Meatballs Tea Towel', '7.49', '12.99', NULL, 0),
(7, 4, 4, 'Lavender Oat Bar Soap', '2.69', '4.99', NULL, 7),
(8, 5, 2, 'Castle Ridge Chardonnay', '13.99', '18.99', NULL, 9),
(9, 5, 2, 'Castle Ridge Cabernet Sauvignon', '13.49', '21.99', NULL, 11),
(10, 6, 1, '80% Cacao and Hazelnut Truffles', '6.35', '8.99', NULL, 6),
(11, 6, 0, 'The Luxury Bar - 60% Cacao', '5.35', '7.99', NULL, 12),
(12, 7, 0, 'The Zesty Cheddar Party Mix', '3.49', '6.89', NULL, 9),
(13, 7, 0, 'Rosemary Garlic Snack Mix', '3.49', '6.89', NULL, 11),
(14, 4, 4, 'Eucalyptus and Mint Liquid Hand Soap', '5.40', '9.89', NULL, 8);

-- --------------------------------------------------------

--
-- Table structure for table `Product_Purchases`
--

CREATE TABLE `Product_Purchases` (
  `pid` int(5) NOT NULL, 
  `purid` int(5) NOT NULL,
  `quantity` int(10) DEFAULT 0,
  PRIMARY KEY (`pid`,`purid`),
  KEY `purid` (`purid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Product_Purchases`
--

INSERT INTO `Product_Purchases` (`pid`, `purid`, `quantity`) VALUES
(0, 0, 8),
(1, 7, 11),
(2, 1, 9),
(3, 1, 9),
(4, 2, 12),
(5, 2, 12),
(7, 3, 11),
(8, 4, 11),
(9, 4, 11),
(10, 5, 8),
(11, 5, 14),
(12, 6, 12),
(13, 6, 12),
(14, 8, 12);

-- --------------------------------------------------------

--
-- Table structure for table `Product_Sales`
--

CREATE TABLE `Product_Sales` (
  `pid` int(5) NOT NULL,
  `sid` int(5) NOT NULL,
  `quantity` int(10) NOT NULL DEFAULT 0,
  `refunded` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`pid`,`sid`),
  KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Product_Sales`
--

INSERT INTO `Product_Sales` (`pid`, `sid`, `quantity`, `refunded`) VALUES
(0, 0, 1, 0),
(0, 3, 1, 0),
(1, 4, 1, 0),
(2, 0, 1, 0),
(3, 4, 1, 0),
(7, 0, 2, 0),
(7, 3, 1, 0),
(7, 4, 1, 0),
(8, 1, 1, 0),
(8, 2, 1, 0),
(10, 1, 1, 0),
(10, 2, 1, 0),
(11, 1, 1, 0),
(11, 2, 1, 0),
(12, 1, 1, 0),
(12, 2, 1, 0),
(13, 2, 1, 0),
(14, 3, 2, 0),
(14, 4, 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Purchases`
--

CREATE TABLE `Purchases` (
  `purchaseID` int(5) NOT NULL AUTO_INCREMENT,
  `vid` int(5) NOT NULL,
  `purchaseDate` date NOT NULL,
  `totalPaid` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`purchaseID`),
  KEY `purvid` (`vid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Purchases`
--

INSERT INTO `Purchases` (`purchaseID`, `vid`, `purchaseDate`, `totalPaid`) VALUES
(0, 0, '2021-07-20', '247.86'),
(1, 1, '2021-07-09', '88.67'),
(2, 2, '2021-06-23', '89.47'),
(3, 4, '2021-07-10', '149.67'),
(4, 5, '2021-07-17', '290.76'),
(5, 6, '2021-07-19', '176.54'),
(6, 7, '2021-06-11', '89.55'),
(7, 0, '2021-05-26', '67.78'),
(8, 4, '2021-05-12', '278.89');

-- --------------------------------------------------------

--
-- Table structure for table `Sales`
--

CREATE TABLE `Sales` (
  `saleID` int(5) NOT NULL  AUTO_INCREMENT,
  `cid` int(5) NOT NULL,
  `saleDate` date NOT NULL,
  `totalPrice` decimal(10,2) NOT NULL DEFAULT 0.00,
  `paymentMethod` varchar(255) NOT NULL DEFAULT 'Credit Card',
  PRIMARY KEY (`saleID`),
  KEY `cid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Sales`
--

INSERT INTO `Sales` (`saleID`, `cid`, `saleDate`, `totalPrice`, `paymentMethod`) VALUES
(0, 0, '2021-07-24', '76.97', 'Credit Card'),
(1, 1, '2021-07-31', '67.44', 'Paypal'),
(2, 2, '2021-07-23', '102.34', 'Credit Card'),
(3, 3, '2021-08-05', '96.78', 'Credit Card'),
(4, 2, '2021-08-03', '99.67', 'Credit Card');

-- --------------------------------------------------------

--
-- Table structure for table `Vendors`
--

CREATE TABLE `Vendors` (
  `vendorID` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`vendorID`),
  UNIQUE KEY `vendorID` (`vendorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Vendors`
--

INSERT INTO `Vendors` (`vendorID`, `name`, `email`, `description`) VALUES
(0, 'Sea Cliff Glassworks', 'cliff@scglassworks.net', 'Sells stained glass window decorations, figurines, and stemware. '),
(1, 'Unreal Bath Bombs', 'stephanieg@unreal.com', 'Sells a variety of scented bath bombs with bright colors and glitter.'),
(2, 'Daisy Hill Creamery', 'jed@daisyhill.biz', 'Sells cow, goat, and sheep cheeses in a range of styles. '),
(3, 'Tasteful Tea Towels', 'libbythetowellady@yahoo.com', 'Sells handmade embroidered tea towels in a variety of colors that include artsy designs and humorous messages.'),
(4, 'Mill Valley Soap Co.', 'jenv@millvalleysoap.com', 'Sells artisanal bar and liquid soaps with all natural vegan ingredients. '),
(5, 'Castle Ridge Vineyards', 'antoni@castleridge.net', NULL),
(6, 'Butterfly Chocolatiers', 'iheartchocoloate@yahoo.com', 'Sells an assortment of truffles, candies, and chocolate bars with fair trade cacao. '),
(7, 'Sensational Snack Mixes', 'sharonbennet@gmail.com', 'Hand made snack and party mixes coming in a variety of interesting and sophisticated flavors.');

--
-- Constraints for table `Products`
--
ALTER TABLE `Products`
  ADD CONSTRAINT `pcatid` FOREIGN KEY (`catid`) REFERENCES `Categories` (`categoryID`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `pvid` FOREIGN KEY (`vid`) REFERENCES `Vendors` (`vendorID`) ON UPDATE CASCADE;

--
-- Constraints for table `Product_Purchases`
--
ALTER TABLE `Product_Purchases`
  ADD CONSTRAINT `purid` FOREIGN KEY (`purid`) REFERENCES `Purchases` (`purchaseID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `purpid` FOREIGN KEY (`pid`) REFERENCES `Products` (`productID`) ON UPDATE CASCADE;

--
-- Constraints for table `Product_Sales`
--
ALTER TABLE `Product_Sales`
  ADD CONSTRAINT `sid` FOREIGN KEY (`sid`) REFERENCES `Sales` (`saleID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `spid` FOREIGN KEY (`pid`) REFERENCES `Products` (`productID`) ON UPDATE CASCADE;

--
-- Constraints for table `Purchases`
--
ALTER TABLE `Purchases`
  ADD CONSTRAINT `purvid` FOREIGN KEY (`vid`) REFERENCES `Vendors` (`vendorID`) ON UPDATE CASCADE;

--
-- Constraints for table `Sales`
--
ALTER TABLE `Sales`
  ADD CONSTRAINT `cid` FOREIGN KEY (`cid`) REFERENCES `Customers` (`customerID`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
