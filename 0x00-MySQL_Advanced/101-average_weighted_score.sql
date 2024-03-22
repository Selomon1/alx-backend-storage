-- Create the stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	-- Declare variables
	DECLARE total_score FLOAT;
	DECLARE total_weight FLOAT;

	-- Calculate total score and weight
	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
	INTO total_score, total_weight
	FROM corrections
	INNER JOIN projects ON corrections.project_id = projects.id;

	UPDATE users
	SET average_score = total_score / total_weight;

END //
DELIMITER ;
