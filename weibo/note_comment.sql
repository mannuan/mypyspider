DROP TABLE IF EXISTS `note_comment`;
CREATE TABLE `note_comment` (
  `note_id` int(10) NOT NULL,
  `comment_id` bigint(255) NOT NULL,
  `comment_context` text NOT NULL,
  `comment_push_time` varchar(20) NOT NULL,
  `comment_spider_time` varchar(20) NOT NULL,
  `comment_push_person_id` bigint(255) NOT NULL,
  PRIMARY KEY (`note_id`,`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--alter table note_comment modify column comment_id bigint(255) NOT NULL;