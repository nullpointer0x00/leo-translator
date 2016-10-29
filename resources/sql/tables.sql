# noinspection SqlNoDataSourceInspectionForFile
CREATE DATABASE `Uebersetzung`;
USE `Uebersetzung`;
CREATE TABLE `Uebersetzung`.`SearchHistory` (
  `Id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `SearchTerm` VARCHAR(128) NOT NULL,
  `Lang` VARCHAR(2) NOT NULL,
  `Status` VARCHAR(16) DEFAULT NULL,
  `Created` TIMESTAMP DEFAULT now(),
  `Updated` TIMESTAMP DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`));

CREATE TABLE `Uebersetzung`.`EnglishWord` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Word` VARCHAR(256) NOT NULL,
  `Type` VARCHAR(16) NOT NULL,
  `Created` TIMESTAMP DEFAULT now(),
  `Updated` TIMESTAMP DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`),
  UNIQUE INDEX (`Word`)
);

CREATE TABLE `Uebersetzung`.`DeutschWord` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Word` VARCHAR(256) NOT NULL,
  `Type` VARCHAR(16) NOT NULL,
  `Gender` VARCHAR(1),
  `Created` TIMESTAMP DEFAULT now(),
  `Updated` TIMESTAMP DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`),
  UNIQUE INDEX (`Word`)
);

CREATE TABLE `Uebersetzung`.`EnglishDeutschTranslation` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `EnglishWordId` VARCHAR(256) NOT NULL,
  `DeutschWordId` VARCHAR(256) NOT NULL,
  `Created` TIMESTAMP DEFAULT now(),
  `Updated` TIMESTAMP DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`),
  UNIQUE  INDEX (`DeutschWordId`, `EnglishWordId`)
);