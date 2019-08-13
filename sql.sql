CREATE TABLE `novel` (
  `chapter_id` int(11) NOT NULL,
  `content` text,
  `title` varchar(100) DEFAULT NULL,
  `book_id` varchar(32) DEFAULT NULL COMMENT '自定义 不重复即可',
  `site` varchar(100) DEFAULT NULL COMMENT '取网站的host',
  KEY `book_id_index` (`book_id`) /*!80000 INVISIBLE */,
  KEY `chapter_id_index` (`chapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8