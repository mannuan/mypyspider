DROP TABLE IF EXISTS `website`;
CREATE TABLE `website` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `url` varchar(100) NOT NULL,
  `push_time` varchar(50) NOT NULL,
  `spider_time` varchar(50) NOT NULL,
  `come_from` text NOT NULL,
  `context` text NOT NULL,
  `indexed` int(1) DEFAULT '0',
  `page_type` varchar(50) NOT NULL,
  `type_two` int(3) NOT NULL DEFAULT '0',
  `type_one` int(3) NOT NULL DEFAULT '0',
  `type_id` int(5) DEFAULT '0',
  `file_url` varchar(100) DEFAULT NULL,
  `file_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#添加url主键
alter table website modify column id int(10) NOT NULL;
alter table website drop primary key;
alter table website add primary key(id,url);
alter table website modify column id int(10) NOT NULL AUTO_INCREMENT;