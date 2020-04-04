DELIMITER //
DROP PROCEDURE IF EXISTS getUserInfo // 

CREATE PROCEDURE getUserInfo(IN userNameIn VARCHAR(33))
BEGIN
   SELECT *
      FROM users
      WHERE user_name = userNameIn;
END//
DELIMITER ;
