DELIMITER //
DROP PROCEDURE IF EXISTS deleteUserById //

CREATE PROCEDURE deleteUserById(IN id INT)
BEGIN
    DELETE FROM presents WHERE user_id = id;
    DELETE FROM users WHERE user_id = id;
END //
DELIMITER ;