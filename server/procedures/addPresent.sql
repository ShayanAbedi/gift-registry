DELIMITER //
DROP PROCEDURE IF EXISTS addPresent //

CREATE PROCEDURE addPresent(
    IN name VARCHAR(33),IN link VARCHAR(250), IN img VARCHAR(250),IN id VARCHAR(33)
    )
BEGIN
    INSERT INTO presents (present_name, link, img_url, user_id) VALUES (name, link, img, id);
SELECT LAST_INSERT_ID();
END //
DELIMITER ;
