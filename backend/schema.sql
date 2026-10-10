CREATE DATABASE IF NOT EXISTS travelmind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE travelmind;

CREATE TABLE users (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(120) NOT NULL,
 email VARCHAR(255) NOT NULL UNIQUE,
 password_hash VARCHAR(255) NOT NULL,
 preferences JSON,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trips (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 user_id BIGINT NOT NULL,
 origin VARCHAR(120) NOT NULL,
 destination VARCHAR(120) NOT NULL,
 start_date DATE NOT NULL,
 end_date DATE NOT NULL,
 travellers INT DEFAULT 1,
 budget DECIMAL(12,2) DEFAULT 0,
 status ENUM('draft','planned','live','completed','cancelled') DEFAULT 'draft',
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE trip_members (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 user_id BIGINT NOT NULL,
 role ENUM('owner','member') DEFAULT 'member',
 status ENUM('invited','accepted','declined') DEFAULT 'invited',
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
 UNIQUE KEY uq_trip_member(trip_id,user_id)
);

CREATE TABLE flights (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 airline VARCHAR(120),
 flight_number VARCHAR(50),
 departure_time DATETIME,
 arrival_time DATETIME,
 duration VARCHAR(30),
 price DECIMAL(12,2),
 tag VARCHAR(50),
 selected BOOLEAN DEFAULT FALSE,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE hotels (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 name VARCHAR(180),
 rating DECIMAL(2,1),
 price_per_night DECIMAL(12,2),
 distance VARCHAR(80),
 amenities JSON,
 reason TEXT,
 selected BOOLEAN DEFAULT FALSE,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE places (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 name VARCHAR(180),
 category VARCHAR(80),
 rating DECIMAL(2,1),
 latitude DECIMAL(10,7),
 longitude DECIMAL(10,7),
 travel_time VARCHAR(50),
 is_hidden_gem BOOLEAN DEFAULT FALSE,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE itinerary_items (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 day_number INT NOT NULL,
 event_time VARCHAR(20),
 activity VARCHAR(255),
 location VARCHAR(180),
 status ENUM('planned','done','skipped','replaced') DEFAULT 'planned',
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE budget_items (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 category VARCHAR(80),
 amount DECIMAL(12,2),
 description VARCHAR(255),
 planned BOOLEAN DEFAULT TRUE,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE expenses (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 user_id BIGINT,
 category VARCHAR(80),
 amount DECIMAL(12,2),
 description VARCHAR(255),
 spent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE agent_logs (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT,
 agent_name VARCHAR(100),
 status ENUM('working','done','failed') DEFAULT 'working',
 input_data JSON,
 output_data JSON,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE chat_messages (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT,
 user_id BIGINT,
 role ENUM('user','assistant','system') NOT NULL,
 message TEXT NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE live_events (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT NOT NULL,
 event_type VARCHAR(80),
 severity ENUM('info','warning','critical') DEFAULT 'info',
 description TEXT,
 old_plan JSON,
 new_plan JSON,
 resolved BOOLEAN DEFAULT FALSE,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE weather_snapshots (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 trip_id BIGINT,
 location VARCHAR(180),
 temperature DECIMAL(5,2),
 condition_text VARCHAR(120),
 rain_probability DECIMAL(5,2),
 observed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

CREATE TABLE saved_places (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 user_id BIGINT NOT NULL,
 name VARCHAR(180),
 destination VARCHAR(120),
 category VARCHAR(80),
 notes TEXT,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE notifications (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 user_id BIGINT NOT NULL,
 trip_id BIGINT,
 title VARCHAR(180),
 message TEXT,
 type VARCHAR(50),
 is_read BOOLEAN DEFAULT FALSE,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
 FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);
