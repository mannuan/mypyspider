DROP TABLE IF EXISTS `baidubaike`;
CREATE TABLE `baidubaike` (
  `basic_info` text,
  `content` text,
  `crawl_time` varchar(100),
  `pic_url` text,
  `quick_pic` varchar(100),
  `reference` text,
  `river_name` varchar(100) NOT NULL,
  `summary` text,
  `title` varchar(100),
  PRIMARY KEY (`river_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;