DROP TABLE IF EXISTS `weibo_user`;
CREATE TABLE `weibo_user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `uid` varchar(50) NOT NULL,
  `uname` varchar(100) NOT NULL,
  `crawl_time` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;