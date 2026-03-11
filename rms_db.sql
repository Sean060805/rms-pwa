-- --------------------------------------------------------
-- RMS_DB DATABASE DUMP FILE
-- Record Management System
-- Author: Sean Looc
-- Date: 11/11/2025
-- --------------------------------------------------------

-- Create the database
CREATE DATABASE IF NOT EXISTS rms_db;
USE rms_db;

-- --------------------------------------------------------
-- Table structure for `users`
-- --------------------------------------------------------
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fullname` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `user_role` VARCHAR(20) NOT NULL DEFAULT 'User',
  `date_created` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_username` (`username`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Sample admin account
-- Password: admin123
-- --------------------------------------------------------
INSERT INTO `users` (`fullname`, `email`, `username`, `password`, `user_role`)
VALUES (
  'System Administrator',
  'admin@example.com',
  'admin',
  'scrypt:32768:8:1$NATW7w6FrvhAivU4$9fc559743405f1acc84ebeb2d985d659170d406913b5bbd28c10718f5b11fda6900f2b0caa852e8dff0b173ffd39239455f1a12c2dea1cfeecfc3f02dc0fddc2',
  'Admin'
);
