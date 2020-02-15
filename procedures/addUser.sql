DELIMITER //
DROP PROCEDURE IF EXISTS addUser //

CREATE PROCEDURE addUser(
    IN name VARCHAR(33),IN email VARCHAR(50), IN pass VARCHAR(33)
    )
BEGIN
    INSERT INTO users (user_name, email, password) VALUES (name, email, pass);
END //
DELIMITER ;

