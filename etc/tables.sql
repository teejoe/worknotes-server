CREATE TABLE IF NOT EXISTS `worknotes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `cost` decimal(4,2) DEFAULT 0,
  `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uname` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
