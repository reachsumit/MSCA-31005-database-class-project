-- -----------------------------------------------------
-- Schema dbprojectAWS
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `dbprojectAWS` DEFAULT CHARACTER SET latin1 ;
USE `dbprojectAWS` ;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`categories` (
  `category_id` INT(11) NOT NULL,
  `category_name` VARCHAR(45) NULL,
  `shortname` VARCHAR(45) NULL,
  `sort_name` VARCHAR(45) NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`cities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`cities` (
  `city` VARCHAR(45) NULL,
  `city_id` INT(11) NOT NULL,
  `country` VARCHAR(15) NULL,
  `distance` DECIMAL(12,3) NULL,
  `latitude` DECIMAL(12,8) NULL,
  `localized_country_name` VARCHAR(45) NULL,
  `longitude` DECIMAL(12,8) NULL,
  `member_count` INT(11) NULL,
  `ranking` INT(11) NULL,
  `state` VARCHAR(45) NULL,
  `zip` INT(11) NULL,
  PRIMARY KEY (`city_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`main_topics`
-- -----------------------------------------------------
#CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`main_topics` (
#  `main_topic_id` INT(11) NOT NULL,
#  `topic_name` VARCHAR(99) NULL,
#  `topic_key` VARCHAR(99) NULL,
#  `shortname` VARCHAR(99) NULL,
#  `sort_name` VARCHAR(99) NULL,
#  `icon` VARCHAR(499) NULL,
#  `photo` VARCHAR(499) NULL,
#  `category_id` INT(11) NOT NULL,
#  PRIMARY KEY (`main_topic_id`,`category_id`),
#  INDEX `fk_category_main_topics_idx` (`category_id` ASC),
#  CONSTRAINT `fk_category_main_topics_idx`
#    FOREIGN KEY (`category_id`)
#    REFERENCES `dbprojectAWS`.`categories` (`category_id`))
#ENGINE = InnoDB
#DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`topics` (
  `topic_id` INT(11) NOT NULL,
  `description` VARCHAR(499) NULL,
  `link` VARCHAR(99) NULL,
  `members` INT(11) NULL,
  `topic_name` VARCHAR(99) NULL,
#  `updated` DATETIME NULL,
  `urlkey` VARCHAR(99) NULL,
  `main_topic_id` INT(11) NOT NULL,
  PRIMARY KEY (`topic_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;



-- -----------------------------------------------------
-- Table `dbprojectAWS`.`groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`groups` (
  `group_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `category.name` VARCHAR(45) NULL,
  `category.shortname` VARCHAR(45) NULL,
  `city_id` INT(11) NOT NULL,
  `city` VARCHAR(75) NULL,
  `country` VARCHAR(45) NULL,
  `created` DATETIME NULL,
  `description` LONGTEXT NULL,
  `group_photo.base_url` VARCHAR(200) NULL,
  `group_photo.highres_link` VARCHAR(200) NULL,
  `group_photo.photo_id` INT(11) NULL,
  `group_photo.photo_link` VARCHAR(200) NULL,
  `group_photo.thumb_link` VARCHAR(200) NULL,
  `group_photo.type` ENUM('event', 'member', 'others') NULL,
  `join_mode` ENUM('open', 'approval', 'closed', 'others'),
  `lat` DECIMAL(12,8) NULL,
  `link` VARCHAR(450) NULL,
  `lon` DECIMAL(12,8) NULL,
  `members` INT(11) NULL,
  `group_name` VARCHAR(150) NULL,
  `organizer.member_id` INT(11) NULL,
  `organizer.name` VARCHAR(65) NULL,
  `organizer.photo.base_url` VARCHAR(200) NULL,
  `organizer.photo.highres_link` VARCHAR(200) NULL,
  `organizer.photo.photo_id` INT(11) NULL,
  `organizer.photo.photo_link` VARCHAR(200) NULL,
  `organizer.photo.thumb_link` VARCHAR(200) NULL,
  `organizer.photo.type` ENUM('event', 'member', 'others'),
  `rating` DECIMAL(4,2) NULL,
  `state` VARCHAR(45) NULL,
  `timezone` VARCHAR(65) NULL,
#  `topics` VARCHAR(5000) NULL,
  `urlname` VARCHAR(65) NULL,
  `utc_offset` INT(11) NULL,
  `visibility` ENUM('members', 'public', 'public_limited', 'others'),
  `who` VARCHAR(85) NULL,
  PRIMARY KEY (`group_id`),
  CONSTRAINT `fk_groups_cities`
    FOREIGN KEY (`city_id`)
    REFERENCES `dbprojectAWS`.`cities` (`city_id`),
  CONSTRAINT `fk_groups_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `dbprojectAWS`.`categories` (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;



-- -----------------------------------------------------
-- Table `dbprojectAWS`.`groups_topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`groups_topics` (
  `topic_id` INT(11) NOT NULL,
  `topic_key` VARCHAR(60) NULL,
  `topic_name` VARCHAR(60) NULL,
  `group_id` INT(11) NOT NULL,
  PRIMARY KEY (`topic_id`,`group_id`),
  INDEX `fk_groups_topics_idx` (`group_id` ASC),
  CONSTRAINT `fk_groups_topics_idx`
    FOREIGN KEY (`group_id`)
    REFERENCES `dbprojectAWS`.`groups` (`group_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_groups_subtopics_idx`
    FOREIGN KEY (`topic_id`)
    REFERENCES `dbprojectAWS`.`topics` (`topic_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`members` (
  `member_id` INT(11) NOT NULL,
  `bio` VARCHAR(400) NOT NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `hometown` VARCHAR(45) NULL,
  `joined` DATETIME NULL,
  `lat` DECIMAL(12,8) NULL,
  `link` VARCHAR(200) NULL,
  `lon` DECIMAL(12,8) NULL,
  `member_name` VARCHAR(45) NULL,
#  `other_services` VARCHAR(999) NULL,
#  `photo` VARCHAR(999) NULL,
#  `self` VARCHAR(999) NULL,
  `state` VARCHAR(45) NULL,
  `member_status` ENUM('active', 'prereg', 'others') NULL,
#  `topics` VARCHAR(5000) NULL,
  `visited` DATETIME NULL,
  `group_id` INT(11) NOT NULL,
  PRIMARY KEY (`member_id`,`group_id`),
  INDEX `fk_members_groups_idx` (`group_id` ASC),
  CONSTRAINT `fk_members_groups_idx`
    FOREIGN KEY (`group_id`)
    REFERENCES `dbprojectAWS`.`groups` (`group_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`members_topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`members_topics` (
  `topic_id` INT(11) NOT NULL,
  `topic_key` VARCHAR(99) NULL,
  `topic_name` VARCHAR(99) NULL,
  `member_id` INT(11) NOT NULL,
  PRIMARY KEY (`topic_id`,`member_id`),
  INDEX `fk_members_topics_idx` (`member_id` ASC),
  CONSTRAINT `fk_members_topics_idx`
    FOREIGN KEY (`member_id`)
    REFERENCES `dbprojectAWS`.`members` (`member_id`),
  CONSTRAINT `fk_members_topics_topics_idx`
    FOREIGN KEY (`topic_id`)
    REFERENCES `dbprojectAWS`.`topics` (`topic_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbprojectAWS`.`venue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`venues` (
  `venue_id` INT(11) NOT NULL,
  `address_1` VARCHAR(200) NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `distance` DECIMAL(10,2) NULL,
  `lat` DECIMAL(12,8) NULL,
  `localized_country_name` VARCHAR(45) NULL,
  `lon` DECIMAL(12,8) NULL,
  `venue_name` VARCHAR(300) NULL,
  `rating` DECIMAL(5,2) NULL,
  `rating_count` INT(11) NULL,
  `state` VARCHAR(15) NULL,
  `zip` INT(11) NULL,
  PRIMARY KEY (`venue_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`venues_groups`
-- -----------------------------------------------------
#CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`venues_groups` (
#  `venue_id` INT(11) NOT NULL,
#  `group_id` INT(11) NOT NULL,
#  PRIMARY KEY (`venue_id`,`group_id`),
#  INDEX `fk_venues_groups_idx` (`group_id` ASC),
#  CONSTRAINT `fk_venues_groups_venues`
#    FOREIGN KEY (`venue_id`)
#    REFERENCES `dbprojectAWS`.`venues` (`venue_id`)
#    ON DELETE NO ACTION
#    ON UPDATE NO ACTION,
#  CONSTRAINT `fk_venues_groups_groups`
#    FOREIGN KEY (`group_id`)
#    REFERENCES `dbprojectAWS`.`groups` (`group_id`))
#ENGINE = InnoDB
#DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `dbprojectAWS`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbprojectAWS`.`events` (
  `event_id` VARCHAR(75) NOT NULL,
  `created` DATETIME NULL,
  `description` LONGTEXT NULL,
  `duration` INT(11) NULL,
  `event_url` VARCHAR(300) NULL,
  `fee.accepts` ENUM('paypal', 'amazon', 'wepay', 'cash', 'others'),
  `fee.amount` DECIMAL(13,2) NULL,
  `fee.currency` VARCHAR(15) NULL,
  `fee.description` VARCHAR(45) NULL DEFAULT 'per person',
  `fee.label` VARCHAR(45) NULL DEFAULT 'Price',
  `fee.required` TINYINT(4) NULL,
  `group.created` DATETIME NULL,
  `group.group_lat` DECIMAL(12,8) NULL,
  `group.group_lon` DECIMAL(12,8) NULL,
  `group_id` INT(11) NOT NULL,
  `group.join_mode` ENUM('open', 'approval', 'closed', 'others'),
  `group.name` VARCHAR(70) NULL,
  `group.urlname` VARCHAR(90) NULL,
  `group.who` VARCHAR(45) NULL,
  `headcount` INT(11) NULL,
  `how_to_find_us` VARCHAR(250) NULL DEFAULT 'not_found.',
  `maybe_rsvp_count` INT(11) NULL,
  `event_name` VARCHAR(95) NULL,
  `photo_url` VARCHAR(200) NULL,
  `rating.average` DECIMAL(5,2) NULL,
  `rating.count` INT(11) NULL,
  `rsvp_limit` INT(11) NULL,
  `event_status` ENUM('past', 'upcoming', 'others') NULL,
  `event_time` DATETIME NULL,
  `updated` DATETIME NULL,
  `utc_offset` INT(11) NULL,
  `venue.address_1` VARCHAR(200) NULL,
  `venue.address_2` VARCHAR(200) NULL,
  `venue.city` VARCHAR(45) NULL,
  `venue.country` VARCHAR(45) NULL,
  `venue_id` INT(11) NULL,
  `venue.lat` DECIMAL(12,8) NULL,
  `venue.localized_country_name` VARCHAR(45) NULL,
  `venue.lon` DECIMAL(11,8) NULL,
  `venue.name` VARCHAR(300) NULL,
  `venue.phone` BIGINT(20) NULL,
  `venue.repinned` VARCHAR(45) NULL,
  `venue.state` VARCHAR(45) NULL,
  `venue.zip` INT(11) NULL,
  `visibility` ENUM('public', 'public_limited', 'members', 'others') NULL,
  `waitlist_count` INT(11) NULL,
  `why` VARCHAR(500) NULL,
  `yes_rsvp_count` INT(11) NULL,
  PRIMARY KEY (`event_id`),
  CONSTRAINT `fk_events_groups_idx`
    FOREIGN KEY (`group_id`)
    REFERENCES `dbprojectAWS`.`groups` (`group_id`),
  CONSTRAINT `fk_events_venues_idx`
    FOREIGN KEY (`venue_id`)
    REFERENCES `dbprojectAWS`.`venues` (`venue_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

