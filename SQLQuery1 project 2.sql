CREATE DATABASE HabitMate2;
GO

USE HabitMate2;
GO

-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- HABITS TABLE 
CREATE TABLE habits (
    habit_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    habit_name VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    frequency VARCHAR(50),
    created_at DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- HABIT LOGS TABLE
CREATE TABLE habit_logs (
    log_id INT PRIMARY KEY IDENTITY(1,1),
    habit_id INT NOT NULL,
    user_id INT NOT NULL,
    log_date DATE DEFAULT CAST(GETDATE() AS DATE),
    status VARCHAR(50),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- MOOD ENTRIES TABLE (matches your PYTHON CODE)
CREATE TABLE mood_entries (
    mood_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    mood_label VARCHAR(50),
    energy_level INT,
    positivity_level INT,
    date_logged DATE DEFAULT CAST(GETDATE() AS DATE),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

USE HabitMate2;
GO

-- Delete energy_level column
ALTER TABLE mood_entries DROP COLUMN energy_level;
GO

-- Delete positivity_level column
ALTER TABLE mood_entries DROP COLUMN positivity_level;
GO

-- Verify columns are removed
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'mood_entries'
ORDER BY ORDINAL_POSITION;
GO

SELECT * FROM users;
SELECT * FROM habits;
SELECT * FROM habit_logs;
SELECT * FROM mood_entries;

SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'habits';

