DELIMITER //
DROP PROCEDURE IF EXISTS addUser //

CREATE PROCEDURE addUser(
    IN name VARCHAR(33),IN email VARCHAR(50), IN img VARCHAR(255)
    )
BEGIN
    INSERT INTO users (user_name, email, img_url) VALUES (name, email, img);
END //
DELIMITER ;

