CREATE TABLE IF NOT EXISTS `feedback` (
    `comment_id`  INT(11)      NOT NULL AUTO_INCREMENT COMMENT 'the primary key, and unique identifier for each comment',
    `name`        VARCHAR(100) NOT NULL                COMMENT 'the commentators name',
    `email`       VARCHAR(100) NOT NULL                COMMENT 'the commentators email',
    `comment`     VARCHAR(500) NOT NULL                COMMENT 'the text of the comment',
    PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
