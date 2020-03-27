DELIMITER //
DROP PROCEDURE IF EXISTS updateUser//

CREATE PROCEDURE updateUser(IN id INT, IN emailIn VARCHAR(50), IN img VARCHAR(250))
BEGIN
    UPDATE users
    SET email = emailIn, img_url = img
    WHERE user_id = id;
END //
DELIMITER ;