CREATE TABLE IF NOT EXISTS `skills` (
    `skill_id`       INT(11)      NOT NULL AUTO_INCREMENT COMMENT 'the primary key, and unique identifier for each skill',
    `experience_id`  INT(11)      NOT NULL                COMMENT 'a foreign key that references experiences.experience_id',
    `name`           VARCHAR(100) NOT NULL                COMMENT 'the name of the skill',
    `skill_level`    VARCHAR(100) NOT NULL                COMMENT 'the level of the skill; 1 being worst, 10 being best',
    PRIMARY KEY (`skill_id`),  
    FOREIGN KEY (`experience_id`) REFERENCES `experiences`(`experience_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
