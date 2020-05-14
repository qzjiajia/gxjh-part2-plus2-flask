/*
 Navicat Premium Data Transfer

 Source Server         : localhost_xampp_3306
 Source Server Type    : MySQL
 Source Server Version : 100137
 Source Host           : localhost:3306
 Source Schema         : board

 Target Server Type    : MySQL
 Target Server Version : 100137
 File Encoding         : 65001

 Date: 14/05/2020 14:31:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for board
-- ----------------------------
DROP TABLE IF EXISTS `board`;
CREATE TABLE `board`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `timestamp` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of board
-- ----------------------------
INSERT INTO `board` VALUES (1, '5YyX5Lqs5Z+O5biC5a2m6ZmiIOeng+WktOWwj+WIhumYnyDlvKDlk7I=', '2020-05-14 14:30:36');

SET FOREIGN_KEY_CHECKS = 1;
