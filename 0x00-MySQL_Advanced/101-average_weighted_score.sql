-- Create the stored procedure

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	-- Declare variables
	DECLARE total_score FLOAT;
	DECLARE total_weight FLOAT;

	-- Calculate total score and weight
	SELECT SUM(c.score * p.weight), SUM(p.weight)
	INTO total_score, total_weight
	FROM corrections c
	JOIN projects p ON c.project_id = p.id;

	UPDATE users
	SET average_score = total_score / total_weight;

END //

DELIMITER ;
