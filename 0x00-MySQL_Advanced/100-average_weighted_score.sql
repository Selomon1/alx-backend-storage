-- Create stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN `user_id` INT)
BEGIN
	DECLARE total_score FLOAT;
	DECLARE total_weight INT;
	DECLARE avg_score FLOAT;

	-- Calculate total score and total weight for the user
	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
	INTO total_score, total_weight
	FROM corrections
	INNER JOIN projects ON projects.id = corrections.project_id
	WHERE corrections.user_id = user_id;

	-- Calculate avarage weighted score
	IF total_weight > 0 THEN
		set avg_score = total_score / total_weight;
	ELSE
		SET avg_score = 0;
	END IF;

	-- Update the user's average_score in the users table
	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
END //

DELIMITER ;
