DELIMITER //
DROP PROCEDURE IF EXISTS getUsersByName //

CREATE PROCEDURE getUsersByName(IN name VARCHAR(33))
BEGIN
  SELECT *
    FROM users
      WHERE user_name = name;
END //
DELIMITER ;
