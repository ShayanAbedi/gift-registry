DELIMITER //
DROP PROCEDURE IF EXISTS updatePresent //

CREATE PROCEDURE updatePresent(IN id INT, IN name VARCHAR(33), IN linkIn VARCHAR(250), IN img VARCHAR(250))
BEGIN
    UPDATE presents
    SET present_name = name, link = linkIn, img_url = img
    WHERE present_id = id;
END //
DELIMITER ;