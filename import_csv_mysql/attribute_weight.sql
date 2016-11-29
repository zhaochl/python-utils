/*
 Navicat MySQL Data Transfer

 Source Server         : u-mysql
 Source Server Version : 50544
 Source Host           : u-mysql
 Source Database       : news_db

 Target Server Version : 50544
 File Encoding         : utf-8

 Date: 02/25/2016 15:43:12 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `attribute_weight`
-- ----------------------------
DROP TABLE IF EXISTS `attribute_weight`;
CREATE TABLE `attribute_weight` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `category_i` varchar(255) NOT NULL,
  `category_j` varchar(255) NOT NULL,
  `attribute_i` varchar(255) NOT NULL,
  `weight` float NOT NULL,
  `create_time` datetime NOT NULL,
  `status` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
