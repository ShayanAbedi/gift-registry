DELIMITER //
DROP PROCEDURE IF EXISTS getUserInfo // 

CREATE PROCEDURE getUserInfo(IN userIdIn int)
BEGIN
   SELECT *
      FROM users
      WHERE user_id = userIdIn;
END//
DELIMITER ;
