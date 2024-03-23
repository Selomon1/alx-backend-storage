-- Create the stored procedure

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	-- update average_score for each user
	UPDATE users u
	SET u.average_score = (
		SELECT SUM(c.score * p.weight) / SUM(p.weight)
		FROM corrections c
		JOIN projects p ON c.project_id = p.id
		WHERE c.user_id = u.id
	);
END //

DELIMITER ;
