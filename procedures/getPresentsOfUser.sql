DELIMITER //
DROP PROCEDURE IF EXISTS getPresentsOfUser //

CREATE PROCEDURE getPresentsOfUser(IN userIdIn int)
BEGIN
   SELECT *
      FROM presents
      WHERE user_id = userIdIn;
END//
DELIMITER ;
