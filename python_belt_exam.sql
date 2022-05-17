-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema python_belt_exam
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema python_belt_exam
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `python_belt_exam` DEFAULT CHARACTER SET utf8 ;
USE `python_belt_exam` ;

-- -----------------------------------------------------
-- Table `python_belt_exam`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `python_belt_exam`.`usuarios` (
  `usr_id` BIGINT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(90) NOT NULL,
  `password` VARCHAR(150) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`usr_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `python_belt_exam`.`carros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `python_belt_exam`.`carros` (
  `car_id` BIGINT NOT NULL AUTO_INCREMENT,
  `price` INT NOT NULL,
  `model` VARCHAR(45) NOT NULL,
  `make` VARCHAR(45) NOT NULL,
  `year` INT NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `slr_id` BIGINT NOT NULL,
  `byr_id` BIGINT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`car_id`),
  INDEX `fk_carros_usuarios1_idx` (`byr_id` ASC) VISIBLE,
  INDEX `fk_magazines_usuarios1` (`slr_id` ASC) VISIBLE,
  CONSTRAINT `fk_carros_usuarios1`
    FOREIGN KEY (`byr_id`)
    REFERENCES `python_belt_exam`.`usuarios` (`usr_id`),
  CONSTRAINT `fk_magazines_usuarios1`
    FOREIGN KEY (`slr_id`)
    REFERENCES `python_belt_exam`.`usuarios` (`usr_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
