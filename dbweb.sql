/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50631
Source Host           : localhost:3306
Source Database       : dbweb

Target Server Type    : MYSQL
Target Server Version : 50631
File Encoding         : 65001

Date: 2016-10-29 17:04:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('e32426d3e862');

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `topicNum` int(11) DEFAULT NULL,
  `createdTime` datetime DEFAULT NULL,
  `about` text NOT NULL,
  `logo` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of groups
-- ----------------------------
INSERT INTO `groups` VALUES ('1', '新手入门', '3', '2016-09-20 00:00:00', '略', '/static/images/group/1.jpg');
INSERT INTO `groups` VALUES ('2', '策略研究', '0', '2016-10-07 16:55:24', '分享讨论策略', '/static/images/group/4.jpg');
INSERT INTO `groups` VALUES ('3', '讨论', null, '2016-10-14 16:56:03', '大家一起来讨论', '/static/images/group/3.jpg');

-- ----------------------------
-- Table structure for post
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(1024) NOT NULL,
  `topicID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `createdTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topicID` (`topicID`),
  KEY `userID` (`userID`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`topicID`) REFERENCES `topics` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of post
-- ----------------------------
INSERT INTO `post` VALUES ('4', '很好', '3', '2', '2016-10-29 17:01:08');
INSERT INTO `post` VALUES ('5', '板凳', '3', '2', '2016-10-29 17:01:19');
INSERT INTO `post` VALUES ('6', 'nice', '4', '2', '2016-10-29 17:03:29');
INSERT INTO `post` VALUES ('7', '@<a href=\"/user/2/\" class=\"mention\">root</a> good!', '4', '1', '2016-10-29 17:04:05');

-- ----------------------------
-- Table structure for topics
-- ----------------------------
DROP TABLE IF EXISTS `topics`;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `content` text NOT NULL,
  `visitNum` int(11) DEFAULT NULL,
  `postNum` int(11) DEFAULT NULL,
  `groupID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `createdTime` datetime DEFAULT NULL,
  `updatedTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `groupID` (`groupID`),
  KEY `userID` (`userID`),
  CONSTRAINT `topics_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`id`),
  CONSTRAINT `topics_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of topics
-- ----------------------------
INSERT INTO `topics` VALUES ('3', '开启你的量化之旅！', '### 1. 什么是量化投资？\r\n---\r\n知乎上的一个热门Topic，关于如何从一个门外汉开始登堂入室，也许可以给你答案：\r\n学习量化交易如何入门？\r\n他山之石可以攻玉，先进市场的经验总是可以借鉴的。下面的书总结了一个合格的alpha交易系统的结构：\r\nInside the black box（中文版：打开量化投资的黑箱）\r\n\r\n### 2. 理论知识预备\r\n---\r\n金融市场的知识总是越多越好，下面的书单给出了一个比较全面的金融市场知识的覆盖：\r\n债券市场的分析入门： 固定收益证券\r\n如何学习金融工程学： 金融工程学\r\n研究市场的心理：行为金融\r\n时间序列和面板分析： 计量经济学\r\n当然如果你对公司基本面的研究感兴趣，财务会计知识总是需要的，下面的学习资料也许会帮到你：\r\n公司财务的权威： 公司财务原理\r\n期权市场方兴未艾，期货市场如火如荼。要想涉足衍生品市场，下面的书你不该错过：\r\n衍生品的圣经： 期权期货和其他衍生品', '2', '2', '1', '2', '2016-10-29 09:00:59', '2016-10-29 17:00:59');
INSERT INTO `topics` VALUES ('4', '量化分析师的Python日记【第1天：谁来给我讲讲Python？】', '### “谁来给我讲讲Python？”\r\n作为无基础的初学者，只想先大概了解一下Python，随便编个小程序，并能看懂一般的程序，那些什么JAVA啊、C啊、继承啊、异常啊通通不懂怎么办，于是我找了很多资料，写成下面这篇日记，希望以完全初学者的角度入手来认识Python这个在量化领域日益重要的语言\r\n\r\n### 一，熟悉基本\r\n在正式介绍python之前，了解下面两个基本操作对后面的学习是有好处的：\r\n1）基本的输入输出 可以在Python中使用+、-、*、/直接进行四则运算。\r\n\r\n```\r\n1+3*3\r\n```', '4', '2', '1', '2', '2016-10-29 09:03:10', '2016-10-29 17:03:23');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `is_password_reset_link_valid` tinyint(1) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `date_joined` datetime DEFAULT NULL,
  `website` varchar(64) DEFAULT NULL,
  `avatar_url` varchar(64) DEFAULT NULL,
  `telephone` varchar(32) DEFAULT NULL,
  `personal_id` varchar(32) DEFAULT NULL,
  `personal_profile` text,
  `postNum` int(11) NOT NULL,
  `topicNum` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', 'qwer', 'pbkdf2:sha1:1000$INi1RCly$777ad3ac02caef772ef7fb1c90ab59d3f0dd74c4', 'qwer@qq.com', '1', '2016-10-29 17:03:46', '2016-10-29 02:29:18', null, '/static/images/default_avatar.jpg', null, null, null, '3', '1');
INSERT INTO `users` VALUES ('2', 'root', 'pbkdf2:sha1:1000$zJ8HGiAD$2a661922e441c49d0fd3b363804e0791a5c3e171', 'root@qq.com', '1', '2016-10-29 08:58:40', '2016-10-29 08:58:40', null, '/static/images/default_avatar.jpg', null, null, null, '3', '2');
