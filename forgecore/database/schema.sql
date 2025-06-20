-- MySQL schema for ForgeCore

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    length_inches INT NOT NULL,
    `source` VARCHAR(255),
    is_remnant TINYINT(1) DEFAULT 0,
    job_id INT,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

CREATE TABLE IF NOT EXISTS cut_parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_length_inches INT NOT NULL,
    material_id INT,
    job_id INT,
    FOREIGN KEY (material_id) REFERENCES materials (id),
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

CREATE TABLE IF NOT EXISTS drawings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    parsed TINYINT(1) DEFAULT 0,
    flagged TINYINT(1) DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drawing_submittals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    drawing_number VARCHAR(255) NOT NULL,
    job_number VARCHAR(255) NOT NULL,
    description TEXT,
    submitted_by VARCHAR(255) NOT NULL,
    submission_date DATE DEFAULT CURRENT_DATE,
    status ENUM('Submitted','Reviewed','Approved') DEFAULT 'Submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
