DELIMITER //
DROP PROCEDURE IF EXISTS getPresentByIdOfUser //

CREATE PROCEDURE getPresentByIdOfUser(IN userIdIn int ,IN presentIdIn int)
BEGIN
   SELECT *
      FROM presents
      WHERE user_id = userIdIn AND present_id = PresentIdIn;
END//
DELIMITER ;
