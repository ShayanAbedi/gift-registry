DELIMITER //
DROP PROCEDURE IF EXISTS getUserById // 

CREATE PROCEDURE getUserById(IN userIdIn int)
BEGIN
   SELECT user_name
      FROM users
      WHERE user_id = userIdIn;
END//
DELIMITER ;
