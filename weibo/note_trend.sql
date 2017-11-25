DROP TABLE IF EXISTS `note_trend`;
CREATE TABLE `note_trend` (
  `note_id` int(10) NOT NULL,
  `count_time` varchar(20) NOT NULL,
  `look_num` int(10) DEFAULT NULL,
  `comment_num` int(10) DEFAULT NULL,
  `hot` int(10) DEFAULT NULL,
  PRIMARY KEY (`note_id`,`count_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8