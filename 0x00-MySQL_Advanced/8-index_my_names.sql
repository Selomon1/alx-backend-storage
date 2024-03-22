-- Create index idx_name_first on the first letter

-- Ensure the names table exists
CREATE TABLE IF NOT EXISTS names (
	id INT not null AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	first_letter CHAR(1) GENERATED ALWAYS AS (LEFT(name, 1)) STORED,
	PRIMARY KEY (id),
	INDEX idx_name_first (first_letter)
);
