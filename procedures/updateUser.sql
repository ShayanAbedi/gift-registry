DELIMITER //
DROP PROCEDURE IF EXISTS updateUser//

CREATE PROCEDURE updateUser(IN id INT, IN userName VARCHAR(33), IN emailIn VARCHAR(50), IN img VARCHAR(250))
BEGIN
    UPDATE users
    SET user_name = userName, email = emailIn, img_url = img
    WHERE user_id = id;
END //
DELIMITER ;