-- Create the stored procedure
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	-- Calculate and update weighed score for each user
	UPDATE users u
	SET u.average_score = (
		SELECT AVG((c.score * p.weight) / (SELECT SUM(weight) FROM projects))
		FROM corrections c
		JOIN projects p ON c.project_id = p.id
		WHERE c.user_id = u.id
	);
END //
DELIMITER ;
