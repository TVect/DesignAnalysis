/*
Navicat MySQL Data Transfer

Source Server         : mySQL-recommend
Source Server Version : 50096
Source Host           : localhost:3306
Source Database       : design

Target Server Type    : MYSQL
Target Server Version : 50096
File Encoding         : 65001

Date: 2016-06-03 17:45:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for design_object
-- ----------------------------
DROP TABLE IF EXISTS `design_object`;
CREATE TABLE `design_object` (
  `id` int(11) NOT NULL auto_increment,
  `create_date` date NOT NULL,
  `design_id` int(11) NOT NULL,
  `object_no` char(32) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=162314 DEFAULT CHARSET=utf8;
