CREATE DATABASE IF NOT EXISTS idea_manager;
USE idea_manager;

-- Users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ideas
CREATE TABLE ideas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    members VARCHAR(255) DEFAULT NULL,
    description TEXT DEFAULT NULL,
    status ENUM('new', 'in-progress', 'completed') NOT NULL DEFAULT 'new',
    completion_percentage INT NOT NULL DEFAULT 0,
    created_by INT DEFAULT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Members in an idea
CREATE TABLE idea_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idea_id INT,
    member_id INT,
    FOREIGN KEY (idea_id) REFERENCES ideas(id),
    FOREIGN KEY (member_id) REFERENCES users(id)
);
