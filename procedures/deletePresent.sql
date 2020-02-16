DELIMITER //
DROP PROCEDURE IF EXISTS deletePresent //

CREATE PROCEDURE deletePresent(IN id INT)
BEGIN
    DELETE FROM presents
        WHERE 
            present_id = id;
END //
DELIMITER ;