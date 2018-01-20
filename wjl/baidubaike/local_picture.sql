DROP TABLE IF EXISTS `localpicture`;
CREATE TABLE `localpicture` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `url` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;