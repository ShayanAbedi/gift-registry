DELIMITER //
DROP PROCEDURE IF EXISTS updatePresentName //

CREATE PROCEDURE updatePresentName(IN id INT, IN name VARCHAR(33))
BEGIN
    UPDATE presents
    SET present_name = name
    WHERE present_id = id;
END //
DELIMITER ;