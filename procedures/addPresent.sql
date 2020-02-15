DELIMITER //
DROP PROCEDURE IF EXISTS addPresent //

CREATE PROCEDURE addPresent(
    IN name VARCHAR(33),IN link VARCHAR(50), IN id VARCHAR(33)
    )
BEGIN
    INSERT INTO presents (present_name, link, user_id) VALUES (name, link, id);
END //
DELIMITER ;