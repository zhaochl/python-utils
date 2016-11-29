/*
 Navicat MySQL Data Transfer

 Source Server         : u-mysql
 Source Server Version : 50544
 Source Host           : u-mysql
 Source Database       : news_db

 Target Server Version : 50544
 File Encoding         : utf-8

 Date: 02/25/2016 11:56:15 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `category_sim`
-- ----------------------------
DROP TABLE IF EXISTS `category_sim`;
CREATE TABLE `category_sim` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `category_i1` varchar(255) NOT NULL,
  `category_i2` varchar(255) NOT NULL,
  `category_j1` varchar(255) NOT NULL,
  `category_j2` varchar(255) NOT NULL,
  `similarity` float NOT NULL,
  `crate_time` datetime NOT NULL,
  `status` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
