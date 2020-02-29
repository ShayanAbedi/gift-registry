DELIMITER //
DROP PROCEDURE IF EXISTS getUserById // 

CREATE PROCEDURE getUserById(IN userIdIn int)
BEGIN
   SELECT * 
      FROM users
      WHERE user_id = userIdIn;
END//
DELIMITER ;
